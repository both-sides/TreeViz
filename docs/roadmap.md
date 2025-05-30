treeviz/                        ← top-level repo
├── bin/                       
│   └── treeviz                ← thin CLI launcher (chmod +x)
├── docs/
│   ├── usage.md               ← end-user docs & examples
│   └── roadmap.md             ← this roadmap in versioned form
├── examples/
│   └── sample_tree.json       ← example export outputs
├── treeviz/                   ← main package
│   ├── __init__.py
│   ├── cli.py                 ← argparse entrypoint, mode routing
│   ├── config.py              ← default settings (depth limit, styles)
│   ├── model.py               ← `Node` class & tree data structure
│   ├── walker.py              ← filesystem walk + cycle detection  
│   ├── fs_utils.py            ← permission-safe wrappers & error tags  
│   ├── formatter/             ← export formats
│   │   ├── __init__.py
│   │   ├── ascii.py           ← ASCII/Unicode tree printer  
│   │   ├── json.py            ← JSON exporter  
│   │   ├── yaml.py            ← YAML exporter  
│   │   ├── dot.py             ← Graphviz DOT exporter  
│   │   └── html.py            ← collapsible HTML viewer  
│   └── ui/                    ← Urwid TUI  
│       ├── __init__.py
│       ├── widgets.py         ← custom TreeWidget subclasses  
│       └── tui.py             ← main loop, keybindings, lazy load  
├── tests/                     
│   ├── test_walker.py         ← cycle detection, max-depth, streaming  
│   ├── test_fs_utils.py       ← unreadable dirs & symlink loops  
│   ├── test_formatters.py     ← correctness of each export  
│   └── test_tui.py            ← smoke tests on widget expansion  
├── .gitignore
├── LICENSE
├── README.md
├── setup.py                   ← setuptools entry, console_scripts
└── requirements.txt           ← urwid, pyyaml, etc.






### roadmap

| Phase                              | Milestones & Tasks                                                                                                                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Project scaffolding**         | • Initialize repo, `setup.py`, CI (pytest)<br>• Stub out `model.py`, `cli.py`, `config.py`                                                                                      |
| **2. Core tree model & walker**    | • Implement `Node` in `model.py`<br>• Write `walker.py` with:<br>  – recursive `scandir`<br>  – cycle detection (inode/realpath set)<br>  – depth/entry limits from `config.py` |
| **3. ASCII/Unicode formatter**     | • Build `formatter/ascii.py`<br>• Honor `--unicode` flag & width truncation<br>• Integrate into `cli.py` for default output                                                     |
| **4. CLI & flags**                 | • Argparse options: `--max-depth`, `--follow-symlinks`, `--pager`<br>• Hook `ascii`, `json`, `yaml`, `dot`, `html` modes                                                        |
| **5. Error-safe filesystem utils** | • In `fs_utils.py`, wrap permission-sensitive calls<br>• Emit “unreadable” nodes; add `--ignore-errors` flag                                                                    |
| **6. Export-format modules**       | • JSON (`formatter/json.py`)<br>• YAML (`formatter/yaml.py`)<br>• DOT (`formatter/dot.py` + optional `--render`)<br>• HTML (`formatter/html.py` with embedded JS/CSS)           |
| **7. Urwid TUI prototype**         | • Simple static tree in `ui/tui.py`<br>• Expand/collapse via ←/→<br>• Lazy-load children on expansion                                                                           |
| **8. TUI polish & features**       | • Search/filter overlay (`/` key)<br>• File vs. dir icons & color palette<br>• “…” placeholder for pruned subtrees                                                              |
| **9. Testing & QA**                | • Unit tests for all walker edge-cases<br>• Formatter output snapshots<br>• TUI smoke tests with `urwid`’s test utilities                                                       |
| **10. Documentation & examples**   | • Flesh out `docs/usage.md`<br>• Add sample exports in `examples/`<br>• Write a “how-to-extend-with-plugins” guide                                                              |
| **11. Packaging & release**        | • Finalize `setup.py`, PyPI metadata<br>• Publish v0.1.0<br>• Announce in README, include badges                                                                                |

