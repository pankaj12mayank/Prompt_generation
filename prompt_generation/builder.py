from __future__ import annotations

from dataclasses import dataclass

from prompt_generation.ollama_client import chat_completion, load_canonical_structure


@dataclass
class RoughInput:
    project_title: str
    business_objective: str
    target_users: str
    core_features: str
    platform: str
    budget_range: str
    timeline_expectation: str
    region_market: str
    competitors: str
    tech_preference: str
    additional_notes: str

    def to_user_block(self) -> str:
        lines = [
            "## Structured details (from customer)",
            "",
            f"1. Project Title: {self.project_title or '(not provided)'}",
            f"2. Business Objective: {self.business_objective or '(not provided)'}",
            f"3. Target Users: {self.target_users or '(not provided)'}",
            f"4. Core Features: {self.core_features or '(not provided)'}",
            f"5. Platform: {self.platform or '(not provided)'}",
            f"6. Budget Range (optional): {self.budget_range or '(not provided)'}",
            f"7. Timeline Expectation: {self.timeline_expectation or '(not provided)'}",
            f"8. Region/Market: {self.region_market or '(not provided)'}",
            f"9. Competitor / reference products: {self.competitors or '(not provided)'}",
            f"10. Tech preference (optional): {self.tech_preference or '(not provided)'}",
            "",
            "## Additional rough notes",
            "",
            self.additional_notes.strip() or "(none)",
        ]
        return "\n".join(lines)


def build_system_prompt(canonical: str) -> str:
    return f"""You are a senior prompt engineer working for a consulting firm.

Your task: produce ONE complete Markdown document that is a "master agent prompt" for another LLM.

CRITICAL RULES (structure fidelity):
1. Copy the EXACT section order, headings, separators (---), and bullet structure from the CANONICAL STRUCTURE below. Do not rename sections, merge them, or skip any.
2. Preserve every numbered item under INPUT COLLECTION (1–10) and every PROCESS STEP (Step 1–10) with the same sub-bullets as in the canonical text.
3. Preserve OUTPUT FORMAT (folder tree), FORMATTING RULES, POST-GENERATION REVIEW, OUTPUT MODE, CONSTRAINTS, and FINAL INSTRUCTION verbatim in meaning; you may only tighten wording if it stays equivalent—prefer verbatim.
4. Customize content using ONLY facts inferable from the customer's input. Where the customer left gaps, keep the INPUT COLLECTION as instructions to ask the user, or add "(to be confirmed)" in brief—do not invent budgets, deadlines, or features.
5. After ROLE and GOAL, insert a short "## Project context (embedded)" subsection (2–6 bullets) summarizing the customer's project so the downstream agent stays anchored. This is the only new top-level block you may add, and it must appear immediately after GOAL's bullet list and before INPUT COLLECTION.
6. No emojis. No AI hype. Professional tone.
7. Output ONLY the final Markdown document. No preamble or postscript.

CANONICAL STRUCTURE (must match this skeleton; fill project-specific parts only where appropriate):

{canonical}
"""


async def generate_master_prompt(rough: RoughInput) -> str:
    canonical = load_canonical_structure()
    system = build_system_prompt(canonical)
    user = (
        rough.to_user_block()
        + "\n\nGenerate the full master prompt Markdown now, following all CRITICAL RULES."
    )
    return await chat_completion(system, user, temperature=0.15)
