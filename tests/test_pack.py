"""The pack hangs together: it builds a brain, and its eval cases name real sections, demo
users and tools. Runs with no model and no network beyond the installed packages."""

from pathlib import Path

import anyio
import pytest
from core.access import RolePolicy, load_dev_users
from core.api.app import build_context
from core.config import Settings, load_pack
from core.evals import load_cases
from core.llm import default_factory

from mcp_server.server import build_server

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BRAIN_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("BRAIN_JWT_SECRET", "test-secret-for-unit-tests-only-0123456789")


def test_the_pack_builds_a_complete_brain() -> None:
    context = build_context(Settings(pack=ROOT), default_factory())
    assert context.pack.config.name == "Skilvanta"


def test_eval_cases_name_real_sections_users_and_tools() -> None:
    pack = load_pack(ROOT)
    docs_root = ROOT / "docs"
    docs = {p.relative_to(docs_root).as_posix() for p in docs_root.rglob("*.md")}
    sections = {
        f"{name}#{line.lstrip('#').strip()}"
        for name in docs
        for line in (docs_root / name).read_text(encoding="utf-8").splitlines()
        if line.startswith("## ")
    }
    assert pack.config.access is not None and pack.config.access.dev_users is not None
    users = load_dev_users(ROOT / pack.config.access.dev_users)
    tools = {t.name for t in anyio.run(build_server().list_tools)}
    for case in load_cases(pack.eval_cases):
        for expected in (*case.expect.retrieves, *case.expect.cites):
            assert expected in (sections if "#" in expected else docs), (case.id, expected)
        assert case.user is None or case.user in users, (case.id, case.user)
        for tool in (*(case.expect.calls or ()), *(case.expect.asks_approval or ())):
            assert tool in tools, (case.id, tool)


def test_the_policy_only_grants_tools_the_server_offers() -> None:
    pack = load_pack(ROOT)
    assert pack.config.access is not None
    policy = RolePolicy.load(ROOT / pack.config.access.policy)
    offered = {t.name for t in anyio.run(build_server().list_tools)}
    granted = {tool for rules in policy._roles.values() for tool in rules.tools}
    assert granted - {"*"} <= offered
