"""Module for SpaczzRuler."""
from __future__ import annotations

from collections import defaultdict, OrderedDict
from pathlib import Path
from typing import Any, DefaultDict, Dict, Iterable, List, Set, Tuple, Union
import warnings

from spacy.language import Language
from spacy.tokens import Doc, Span
import srsly

from ..exceptions import PatternTypeWarning
from ..matcher import FuzzyMatcher, RegexMatcher
from ..util import ensure_path, read_from_disk, write_to_disk


class SpaczzRuler:
    """The SpaczzRuler adds fuzzy and multi-token regex matches to spaCy Doc.ents.

    It can be combined with other spaCy NER components like the statistical
    EntityRecognizer and/or the EntityRuler to boost accuracy.
    After initialization, the component is typically added to the pipeline
    using nlp.add_pipe.

    Attributes:
        nlp: The shared nlp object to pass the vocab to the matchers
            (not currently used by spaczz matchers) and process fuzzy patterns.
        fuzzy_patterns:
            Patterns added to the matcher. Contains patterns
            and kwargs that should be passed to matching function
            for each labels added.
        regex_patterns:
            Patterns added to the matcher. Contains patterns
            and kwargs that should be passed to matching function
            for each labels added.
        defaults: Kwargs to be used as
            default matching settings for the matchers.
            See FuzzySearcher and RegexSearcher documentation
            for kwarg details.
        fuzzy_matcher: The FuzzyMatcher instance
            the SpaczzRuler will use for fuzzy matching.
        regex_matcher: The RegexMatcher instance
            the SpaczzRuler will use for regex matching.
    """

    name = "spaczz_ruler"

    def __init__(self, nlp: Language, **cfg: Any) -> None:
        """Initialize the spaczz ruler with a Language object and cfg parameters.

        All spaczz ruler cfg parameters are prepended with "spaczz_".
        If spaczz_patterns is supplied here, they need to be a list of spaczz patterns:
        dictionaries with a "label", "pattern", "type", and optional "kwargs" key.
        For example:
        {'label': 'ORG', 'pattern': 'Apple', 'type': 'fuzzy', 'kwargs': {'min_r2': 90}}.


        Args:
            nlp: The shared nlp object to pass the vocab to the matchers
                (not currently used by spaczz matchers) and process fuzzy patterns.
            **cfg: Other config parameters. The SpaczzRuler makes heavy use
                of cfg to pass additional parameters down to the matchers.
                spaczz config parameters start with "spaczz_" to keep them
                from colliding with other cfg components.
                SpaczzRuler cfg components include (with "spaczz_" prepended to them):
                overwrite_ents (bool): Whether to overwrite exisiting Doc.ents
                    with new matches. Default is False.
                fuzzy_config (Union[str, FuzzyConfig]): Config to use with the
                    fuzzy matcher. Default is "default". See FuzzyMatcher/FuzzySearcher
                    documentation for available parameter details.
                regex_config (Union[str, RegexConfig]): Config to use with the
                    regex matcher. Default is "default". See RegexMatcher/RegexSearcher
                    documentation for available parameter details.
                fuzzy_defaults (Dict[str, Any]): Modified default parameters to use with
                    the fuzzy matcher. Default is an empty dictionary -
                    utilizing defaults.
                regex_defaults (Dict[str, Any]): Modified default parameters to use with
                    the regex matcher. Default is an empty dictionary -
                    utilizing defaults. See RegexMatcher/RegexSearcher documentation
                    for parameter details.
                patterns (Iterable[Dict[str, Any]]): Patterns to initialize
                    the ruler with. Default is None.
                If SpaczzRuler is loaded as part of a model pipeline,
                cfg will include all keyword arguments passed to spacy.load.

        Raises:
            TypeError: If spaczz_{name}_defaults passed are not dictionaries.
        """
        self.nlp = nlp
        self.fuzzy_patterns: DefaultDict[
            str,
            DefaultDict[str, Union[List[Doc], List[Dict[str, Union[bool, int, str]]]]],
        ] = defaultdict(lambda: defaultdict(list))
        self.regex_patterns: DefaultDict[str, DefaultDict[str, Any]] = defaultdict(
            lambda: defaultdict(list)
        )  # Not sure why mypy complains when this is typed like fuzzy_patterns.
        self.overwrite = cfg.get("spaczz_overwrite_ents", False)
        default_names = ("spaczz_fuzzy_defaults", "spaczz_regex_defaults")
        self.defaults = {}
        for name in default_names:
            if name in cfg:
                if isinstance(cfg[name], dict):
                    self.defaults[name] = cfg[name]
                else:
                    raise TypeError(
                        (
                            "Defaults must be a dictionary of keyword arguments,",
                            f"not {type(cfg[name])}.",
                        )
                    )
        self.fuzzy_matcher = FuzzyMatcher(
            nlp.vocab,
            cfg.get("spaczz_fuzzy_config", "default"),
            **self.defaults.get("spaczz_fuzzy_defaults", {}),
        )
        self.regex_matcher = RegexMatcher(
            nlp.vocab,
            cfg.get("spaczz_fuzzy_config", "default"),
            **self.defaults.get("spaczz_regex_defaults", {}),
        )
        patterns = cfg.get("spaczz_patterns")
        if patterns is not None:
            self.add_patterns(patterns)

    def __call__(self, doc: Doc) -> Doc:
        """Find matches in document and add them as entities.

        Args:
            doc: The Doc object in the pipeline.

        Returns:
            The Doc with added entities, if available.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> doc = nlp.make_doc("My name is Anderson, Grunt")
            >>> ruler.add_patterns([{"label": "NAME", "pattern": "Grant Andersen",
                "type": "fuzzy", "kwargs": {"fuzzy_func": "token_sort"}}])
            >>> doc = ruler(doc)
            >>> "Anderson, Grunt" in [ent.text for ent in doc.ents]
            True
        """
        matches = list(self.fuzzy_matcher(doc) + self.regex_matcher(doc))
        unique_matches = set(
            [(m_id, start, end) for m_id, start, end in matches if start != end]
        )
        sorted_matches = sorted(
            unique_matches, key=lambda m: (m[2] - m[1], m[1]), reverse=True
        )
        entities = list(doc.ents)
        new_entities = []
        seen_tokens: Set[int] = set()
        for match_id, start, end in sorted_matches:
            if any(t.ent_type for t in doc[start:end]) and not self.overwrite:
                continue
            # check for end - 1 here because boundaries are inclusive
            if start not in seen_tokens and end - 1 not in seen_tokens:
                span = Span(doc, start, end, label=match_id)
                new_entities.append(span)
                entities = [
                    e for e in entities if not (e.start < end and e.end > start)
                ]
                seen_tokens.update(range(start, end))
        doc.ents = entities + new_entities
        return doc

    def __contains__(self, label: str) -> bool:
        """Whether a label is present in the patterns."""
        return label in self.fuzzy_patterns or label in self.regex_patterns

    def __len__(self) -> int:
        """The number of all patterns added to the ruler."""
        n_fuzzy_patterns = sum(len(p["patterns"]) for p in self.fuzzy_patterns.values())
        n_regex_patterns = sum(len(p["patterns"]) for p in self.regex_patterns.values())
        return n_fuzzy_patterns + n_regex_patterns

    @property
    def labels(self) -> Tuple[str, ...]:
        """All labels present in the ruler.

        Returns:
            The unique string labels as a tuple.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> ruler.labels
            ('AUTHOR',)
        """
        keys = set(self.fuzzy_patterns.keys())
        keys.update(self.regex_patterns.keys())
        return tuple(keys)

    @property
    def patterns(self) -> List[Dict[str, Any]]:
        """Get all patterns and kwargs that were added to the ruler.

        Returns:
            The original patterns and kwargs,
            one dictionary for each combination.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "STREET", "pattern": "street_addresses",
                "type": "regex", "kwargs": {"predef": True}}])
            >>> ruler.patterns == [
                {
                    "label": "STREET",
                    "pattern": "street_addresses",
                    "type": "regex",
                    "kwargs": {"predef": True},
                    },
                    ]
            True
        """
        all_patterns = []
        for label, patterns in self.fuzzy_patterns.items():
            for pattern, kwargs in zip(patterns["patterns"], patterns["kwargs"]):
                p = {"label": label, "pattern": pattern.text, "type": "fuzzy"}
                if kwargs:
                    p["kwargs"] = kwargs
                all_patterns.append(p)
        for label, patterns in self.regex_patterns.items():
            for pattern, kwargs in zip(patterns["patterns"], patterns["kwargs"]):
                p = {"label": label, "pattern": pattern, "type": "regex"}
                if kwargs:
                    p["kwargs"] = kwargs
                all_patterns.append(p)
        return all_patterns

    def add_patterns(self, patterns: Iterable[Dict[str, Any]],) -> None:
        """Add patterns to the ruler.

        A pattern must be a spaczz pattern:
        {label (str), pattern (str), type (str), and optional kwargs (Dict[str, Any])}.
        For example:
        {"label": "ORG", "pattern": "Apple", "type": "fuzzy", "kwargs": {"min_r2": 90}}

        To utilize regex flags, use inline flags.

        See FuzzyMatcher/FuzzySearcher and RegexMatcher/RegexSearcher documentation
        for details on available kwargs.

        Args:
            patterns: The spaczz patterns to add.

        Raises:
            TypeError: If patterns is not an iterable of dictionaries.
            ValueError: If one or more patterns do not conform
                the spaczz pattern structure.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> "AUTHOR" in ruler.labels
            True
        """
        # disable the nlp components after this one
        # in case they haven't been initialized / deserialised yet
        try:
            current_index = self.nlp.pipe_names.index(self.name)
            subsequent_pipes = [
                pipe for pipe in self.nlp.pipe_names[current_index + 1 :]
            ]
        except ValueError:
            subsequent_pipes = []
        with self.nlp.disable_pipes(subsequent_pipes):
            fuzzy_pattern_labels = []
            fuzzy_pattern_texts = []
            fuzzy_pattern_kwargs = []
            regex_pattern_labels = []
            regex_pattern_texts = []
            regex_pattern_kwargs = []
            for entry in patterns:
                try:
                    if isinstance(entry, dict):
                        if entry["type"] == "fuzzy":
                            fuzzy_pattern_labels.append(entry["label"])
                            fuzzy_pattern_texts.append(entry["pattern"])
                            fuzzy_pattern_kwargs.append(entry.get("kwargs", {}))
                        elif entry["type"] == "regex":
                            regex_pattern_labels.append(entry["label"])
                            regex_pattern_texts.append(entry["pattern"])
                            regex_pattern_kwargs.append(entry.get("kwargs", {}))
                        else:
                            warnings.warn(
                                f"""Spaczz pattern "type" must be "fuzzy" or "regex",\n
                                not {entry["label"]}. Skipping this pattern.""",
                                PatternTypeWarning,
                            )
                    else:
                        raise TypeError(
                            f"Patterns must be an iterable of dicts, not type{patterns}"
                        )
                except KeyError:
                    raise ValueError(
                        (
                            "One or more patterns do not conform",
                            "to spaczz pattern structure:",
                            "{label (str), pattern (str), type (str),",
                            "and optional kwargs (Dict[str, Any])}",
                        )
                    )
            fuzzy_patterns = []
            for label, pattern, kwargs in zip(
                fuzzy_pattern_labels,
                self.nlp.pipe(fuzzy_pattern_texts),
                fuzzy_pattern_kwargs,
            ):
                fuzzy_pattern = {"label": label, "pattern": pattern, "kwargs": kwargs}
                fuzzy_patterns.append(fuzzy_pattern)
            for entry in fuzzy_patterns:
                self.fuzzy_patterns[entry["label"]]["patterns"].append(entry["pattern"])
                self.fuzzy_patterns[entry["label"]]["kwargs"].append(entry["kwargs"])
            regex_patterns = []
            for label, pattern, kwargs in zip(
                regex_pattern_labels, regex_pattern_texts, regex_pattern_kwargs
            ):
                regex_pattern = {"label": label, "pattern": pattern, "kwargs": kwargs}
                regex_patterns.append(regex_pattern)
            for entry in regex_patterns:
                self.regex_patterns[entry["label"]]["patterns"].append(entry["pattern"])
                self.regex_patterns[entry["label"]]["kwargs"].append(entry["kwargs"])
            for label, pattern in self.fuzzy_patterns.items():
                self.fuzzy_matcher.add(label, pattern["patterns"], pattern["kwargs"])
            for label, pattern in self.regex_patterns.items():
                self.regex_matcher.add(label, pattern["patterns"], pattern["kwargs"])

    def from_bytes(self, patterns_bytes: bytes, **kwargs: Any) -> SpaczzRuler:
        """Load the spaczz ruler from a bytestring.

        Args:
            patterns_bytes : The bytestring to load.
            **kwargs: Other config paramters, mostly for consistency.

        Returns:
            The loaded spaczz ruler.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> ruler_bytes = ruler.to_bytes()
            >>> new_ruler = SpaczzRuler(nlp)
            >>> new_ruler = new_ruler.from_bytes(ruler_bytes)
            >>> "AUTHOR" in new_ruler
            True
        """
        cfg = srsly.msgpack_loads(patterns_bytes)
        if isinstance(cfg, dict):
            self.add_patterns(cfg.get("spaczz_patterns", cfg))
            self.defaults = cfg.get("spaczz_defaults", {})
            self.overwrite = cfg.get("spaczz_overwrite", False)
        else:
            self.add_patterns(cfg)
        return self

    def to_bytes(self, **kwargs: Any) -> bytes:
        """Serialize the spaczz ruler patterns to a bytestring.

        Args:
            **kwargs: Other config paramters, mostly for consistency.

        Returns:
            The serialized patterns.

        Example:
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> ruler_bytes = ruler.to_bytes()
            >>> isinstance(ruler_bytes, bytes)
            True
        """
        serial = OrderedDict(
            (
                ("spaczz_overwrite", self.overwrite),
                ("spaczz_patterns", self.patterns),
                ("spaczz_defaults", self.defaults),
            )
        )
        return srsly.msgpack_dumps(serial)

    def from_disk(self, path: Union[str, Path], **kwargs: Any) -> SpaczzRuler:
        """Load the spaczz ruler from a file.

        Expects a file containing newline-delimited JSON (JSONL)
        with one entry per line.

        Args:
            path: The JSONL file to load.
            **kwargs: Other config paramters, mostly for consistency.

        Returns:
            The loaded spaczz ruler.

        Example:
            >>> import os
            >>> import tempfile
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> with tempfile.TemporaryDirectory() as tmpdir:
            >>>     ruler.to_disk(f"{tmpdir}/ruler")
            >>>     new_ruler = SpaczzRuler(nlp)
            >>>     new_ruler = new_ruler.from_disk(f"{tmpdir}/ruler")
            >>> "AUTHOR" in new_ruler
            True
        """
        path = ensure_path(path)
        depr_patterns_path = path.with_suffix(".jsonl")
        if depr_patterns_path.is_file():
            patterns = srsly.read_jsonl(depr_patterns_path)
            self.add_patterns(patterns)
        else:
            cfg = {}
            deserializers_patterns = {
                "spaczz_patterns": lambda p: self.add_patterns(
                    srsly.read_jsonl(p.with_suffix(".jsonl"))
                )
            }
            deserializers_cfg = {"cfg": lambda p: cfg.update(srsly.read_json(p))}
            read_from_disk(path, deserializers_cfg, {})
            self.overwrite = cfg.get("spaczz_overwrite", False)
            self.defaults = cfg.get("spaczz_defaults", {})
            read_from_disk(path, deserializers_patterns, {})
        return self

    def to_disk(self, path: Union[str, Path], **kwargs: Any) -> None:
        """Save the spaczz ruler patterns to a directory.

        The patterns will be saved as newline-delimited JSON (JSONL).

        Args:
            path: The JSONL file to save.
            **kwargs: Other config paramters, mostly for consistency.

        Example:
            >>> import os
            >>> import tempfile
            >>> import spacy
            >>> from spaczz.pipeline import SpaczzRuler
            >>> nlp = spacy.blank("en")
            >>> ruler = SpaczzRuler(nlp)
            >>> ruler.add_patterns([{"label": "AUTHOR", "pattern": "Kerouac",
                "type": "fuzzy"}])
            >>> with tempfile.TemporaryDirectory() as tmpdir:
            >>>     ruler.to_disk(f"{tmpdir}/ruler")
            >>>     isdir = os.path.isdir(f"{tmpdir}/ruler")
            >>> isdir
            True
        """
        path = ensure_path(path)
        cfg = {"spaczz_overwrite": self.overwrite, "spaczz_defaults": self.defaults}
        serializers = {
            "spaczz_patterns": lambda p: srsly.write_jsonl(
                p.with_suffix(".jsonl"), self.patterns
            ),
            "cfg": lambda p: srsly.write_json(p, cfg),
        }
        if path.suffix == ".jsonl":  # user wants to save only JSONL
            srsly.write_jsonl(path, self.patterns)
        else:
            write_to_disk(path, serializers, {})
