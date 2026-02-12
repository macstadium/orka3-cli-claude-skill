#!/usr/bin/env python3
"""
Orka3 CLI Skill A/B Test Harness

Usage:
  1. Run: python3 test-harness.py setup v1   # Install v1 (monolithic)
  2. Start new Claude Code session, run test queries
  3. Run: python3 test-harness.py setup v2   # Install v2 (restructured)
  4. Start new Claude Code session, run same queries
  5. Run: python3 test-harness.py analyze    # Compare results
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


def normalize(text: str) -> str:
    """Strip punctuation and extra whitespace for fuzzy matching."""
    return re.sub(r'[^\w\s]', '', text.lower()).strip()

# Paths
HOME = Path.home()
SKILL_DIR = HOME / ".claude" / "skills" / "orka3-cli"
V1_BACKUP = Path("/tmp/orka3-skill-v1-backup")
V2_BACKUP = Path("/tmp/orka3-skill-backup")
V3_BACKUP = Path("/tmp/orka3-skill-v3-backup")
REPO_SKILL_DIR = Path(__file__).parent / "skill"
SESSIONS_DIR = HOME / ".claude" / "projects"

# Test queries (subset for quick testing)
TEST_QUERIES = [
    ("Q1", "Tier 1", "Deploy a VM with macOS Sonoma"),
    ("Q2", "Tier 1", "Show me all my VMs"),
    ("Q3", "Tier 1", "How do I connect to my VM?"),
    ("Q5", "Tier 2", "Set up a service account for Jenkins"),
    ("Q8", "Tier 3", "How do I create a golden image for my team?"),
    ("Q12", "Tier 4", "Who has access to the production namespace?"),
    ("Q18", "Tier 6", "I'm getting an authentication error"),
    ("Q22", "Tier 7", "How do I suspend an Intel VM?"),
    ("Q25", "Tier 8", "Best practices for remote developers using Orka?"),
    ("Q27", "Tier 8", "Where can I find audit logs for VM operations?"),
]


def setup_skill(version: str):
    """Install specified skill version."""
    if version == "v1":
        source = V1_BACKUP
        desc = "monolithic (708-line SKILL.md)"
    elif version == "v2":
        source = V2_BACKUP
        desc = "restructured (current installed)"
    elif version == "v3":
        source = V3_BACKUP
        desc = "rewritten (~216-line SKILL.md + fixed refs)"
        # Auto-create v3 backup from repo if it doesn't exist
        if not source.exists() and REPO_SKILL_DIR.exists():
            print(f"Creating v3 backup from repo skill/ directory...")
            shutil.copytree(REPO_SKILL_DIR, source)
    else:
        print(f"Unknown version: {version}. Use 'v1', 'v2', or 'v3'")
        sys.exit(1)

    if not source.exists():
        print(f"Error: Backup not found at {source}")
        if version == "v3":
            print("Run from the orka3-cli-claude-skill repo directory.")
        else:
            print("Run the skill backup commands first.")
        sys.exit(1)

    # Clear and copy
    if SKILL_DIR.exists():
        shutil.rmtree(SKILL_DIR)
    shutil.copytree(source, SKILL_DIR)

    # Write version marker for session analysis
    (SKILL_DIR / ".skill-version").write_text(version)

    # Verify
    refs = list((SKILL_DIR / "references").iterdir()) if (SKILL_DIR / "references").exists() else []
    ref_names = [r.name for r in refs]

    print(f"\n{'='*50}")
    print(f"Installed {version.upper()} ({desc}) skill")
    print(f"{'='*50}")
    print(f"Reference structure: {ref_names}")
    print(f"\nNow start a NEW Claude Code session and run these queries:")
    print("-" * 50)
    for qid, tier, query in TEST_QUERIES:
        print(f"  {qid} ({tier}): \"{query}\"")
    print("-" * 50)
    print(f"\nAfter testing, run: python3 {__file__} analyze")


def find_recent_sessions(hours: int = 2) -> list:
    """Find session files modified in the last N hours."""
    cutoff = datetime.now() - timedelta(hours=hours)
    sessions = []

    for project_dir in SESSIONS_DIR.iterdir():
        if project_dir.is_dir():
            for jsonl in project_dir.glob("*.jsonl"):
                if jsonl.name.startswith("agent-"):
                    continue
                mtime = datetime.fromtimestamp(jsonl.stat().st_mtime)
                if mtime > cutoff:
                    sessions.append((jsonl, mtime))

    return sorted(sessions, key=lambda x: x[1], reverse=True)


def detect_installed_version() -> str:
    """Read the version marker from the installed skill."""
    marker = SKILL_DIR / ".skill-version"
    if marker.exists():
        return marker.read_text().strip()
    return "unknown"


def analyze_session(session_path: Path) -> dict:
    """Analyze a session for skill-related tool calls."""
    results = {
        "path": str(session_path),
        "queries": [],
        "skill_reads": [],
        "version": "unknown",
        "total_reads": 0,
        "skill_md_reads": 0,
        "ref_reads": 0,
    }

    current_query = None
    query_reads = defaultdict(list)
    reads_installed_skill = False  # True if session reads from ~/.claude/skills/

    with open(session_path, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                msg = entry.get('message', {})

                # Detect skill version from file paths
                if msg.get('role') == 'assistant':
                    content = msg.get('content', [])
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get('type') == 'tool_use':
                                if item.get('name') == 'Read':
                                    path = item.get('input', {}).get('file_path', '')
                                    if 'orka3-cli' in path or 'orka3-cli' in path.lower():
                                        # Handle both repo paths and installed skill paths
                                        is_installed_skill = '/.claude/skills/orka3-cli/' in path
                                        if is_installed_skill:
                                            short_path = path.split('orka3-cli/')[-1]
                                        elif '/Code/orka3-cli-claude-skill/skill/' in path:
                                            short_path = path.split('/skill/')[-1]
                                        else:
                                            short_path = path.split('orka3-cli/')[-1]
                                        results['skill_reads'].append(short_path)
                                        results['total_reads'] += 1
                                        if is_installed_skill:
                                            reads_installed_skill = True

                                        if short_path == 'SKILL.md':
                                            results['skill_md_reads'] += 1
                                        else:
                                            results['ref_reads'] += 1

                                        # Detect version from path patterns
                                        if '/commands/' in path or '/workflows/' in path or '/troubleshooting/' in path:
                                            if 'command-reference.md' in path or path.endswith('workflows.md') or path.endswith('troubleshooting.md'):
                                                results['version'] = 'v1'
                                            else:
                                                # v2 and v3 share same structure;
                                                # will be overridden by marker below
                                                if results['version'] == 'unknown':
                                                    results['version'] = 'v2'

                                        if current_query:
                                            query_reads[current_query].append(short_path)

                # Track user queries
                if entry.get('type') == 'user':
                    content = msg.get('content', '')
                    if isinstance(content, str) and len(content) > 10:
                        # Check if it matches a test query (punctuation-stripped)
                        norm_content = normalize(content)
                        for qid, tier, query in TEST_QUERIES:
                            if normalize(query) in norm_content:
                                current_query = qid
                                results['queries'].append(qid)
                                break

            except json.JSONDecodeError:
                pass

    # Use version marker for sessions that read from the installed skill
    if reads_installed_skill and results['total_reads'] > 0:
        marker_version = detect_installed_version()
        if marker_version in ('v1', 'v2', 'v3'):
            results['version'] = marker_version

    results['query_reads'] = dict(query_reads)
    return results


def analyze():
    """Analyze recent sessions and compare v1 vs v2."""
    print("\n" + "="*60)
    print("ANALYZING RECENT SESSIONS")
    print("="*60)

    sessions = find_recent_sessions(hours=4)

    if not sessions:
        print("No recent sessions found. Run some tests first!")
        return

    print(f"\nFound {len(sessions)} recent sessions:\n")

    v1_results = []
    v2_results = []
    v3_results = []

    for session_path, mtime in sessions[:10]:  # Check last 10
        results = analyze_session(session_path)

        if results['total_reads'] > 0:  # Only sessions that used the skill
            time_str = mtime.strftime("%H:%M:%S")
            version = results['version']

            print(f"  {time_str} | {version.upper():3} | {results['total_reads']:2} reads | queries: {results['queries']}")

            if version == 'v1':
                v1_results.append(results)
            elif version == 'v2':
                v2_results.append(results)
            elif version == 'v3':
                v3_results.append(results)

    # Summary comparison
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)

    def summarize(results_list, label):
        if not results_list:
            print(f"\n{label}: No data")
            return

        total_reads = sum(r['total_reads'] for r in results_list)
        total_queries = sum(len(r['queries']) for r in results_list)
        skill_md = sum(r['skill_md_reads'] for r in results_list)
        refs = sum(r['ref_reads'] for r in results_list)

        all_files = []
        for r in results_list:
            all_files.extend(r['skill_reads'])
        unique_files = set(all_files)

        print(f"\n{label}:")
        print(f"  Sessions analyzed: {len(results_list)}")
        print(f"  Test queries matched: {total_queries}")
        print(f"  Total skill reads: {total_reads}")
        print(f"    - SKILL.md: {skill_md}")
        print(f"    - Reference files: {refs}")
        if total_queries > 0:
            print(f"  Avg reads per query: {total_reads / total_queries:.2f}")
        print(f"  Unique files accessed: {len(unique_files)}")
        for f in sorted(unique_files):
            print(f"    - {f}")

    summarize(v1_results, "V1 (MONOLITHIC)")
    summarize(v2_results, "V2 (RESTRUCTURED)")
    summarize(v3_results, "V3 (REWRITTEN)")

    # Verdict
    all_versions = {}
    if v1_results:
        all_versions['V1'] = sum(r['total_reads'] for r in v1_results) / max(1, sum(len(r['queries']) for r in v1_results))
    if v2_results:
        all_versions['V2'] = sum(r['total_reads'] for r in v2_results) / max(1, sum(len(r['queries']) for r in v2_results))
    if v3_results:
        all_versions['V3'] = sum(r['total_reads'] for r in v3_results) / max(1, sum(len(r['queries']) for r in v3_results))

    if len(all_versions) >= 2:
        print("\n" + "="*60)
        print("VERDICT")
        print("="*60)
        for name, avg in sorted(all_versions.items()):
            print(f"  {name} avg reads/query: {avg:.2f}")

        best = min(all_versions, key=all_versions.get)
        worst = max(all_versions, key=all_versions.get)
        ratio = all_versions[worst] / all_versions[best] if all_versions[best] > 0 else float('inf')
        print(f"\n  {best} uses {ratio:.1f}x FEWER tool calls than {worst}")
        print(f"  Most efficient: {best}")


def print_queries():
    """Print the test queries for easy copy/paste."""
    print("\n" + "="*60)
    print("TEST QUERIES")
    print("="*60)
    for qid, tier, query in TEST_QUERIES:
        print(f"\n{qid} ({tier}):")
        print(f"  {query}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nCommands:")
        print("  setup v1    - Install v1 (monolithic, 708-line SKILL.md)")
        print("  setup v2    - Install v2 (restructured, current)")
        print("  setup v3    - Install v3 (rewritten ~216-line SKILL.md + fixed refs)")
        print("  analyze     - Analyze recent sessions and compare")
        print("  queries     - Print test queries for copy/paste")
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "setup" and len(sys.argv) > 2:
        setup_skill(sys.argv[2])
    elif cmd == "analyze":
        analyze()
    elif cmd == "queries":
        print_queries()
    else:
        print(f"Unknown command: {cmd}")
        print("Use: setup v1, setup v2, setup v3, analyze, or queries")
        sys.exit(1)


if __name__ == "__main__":
    main()
