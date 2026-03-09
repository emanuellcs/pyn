import time
from typing import Dict, Any
from zxcvbn import zxcvbn
from app.core.domain.password import PasswordDomain
from app.infrastructure.hibp import HIBPService


class PasswordApplicationService:
    @staticmethod
    def analyze(password: str, check_pwned: bool = True) -> Dict[str, Any]:
        if not password:
            return {
                "strength": "Unknown",
                "details": [
                    {"title": "Error", "explanation": "Password cannot be empty."}
                ],
            }

        start_time = time.time()

        # Domain Logic
        entropy_data = PasswordDomain.calculate_entropy(password)
        charset_size, char_sets_used = PasswordDomain.get_charset_size(password)
        crack_time_estimates = PasswordDomain.calculate_crack_time(password)
        complexity = PasswordDomain.check_complexity_requirements(password)

        # Third-party lib
        zxcvbn_results = zxcvbn(password)

        # Infrastructure logic
        pwned_count = HIBPService.check_pwned(password) if check_pwned else -2

        calc_time_ms = (time.time() - start_time) * 1000

        def get_strength_from_score(score: int) -> str:
            return ["Weak", "Weak", "Good", "Strong", "Very Strong"][
                min(max(score, 0), 4)
            ]

        report = {
            "password_strength_metrics": {
                "entropy": entropy_data.get("entropy"),
                "expected_guesses": entropy_data.get("expected_guesses"),
            },
            "crack_time_estimates": crack_time_estimates,
            "complexity_requirements": complexity,
            "zxcvbn_analysis": {
                "score": zxcvbn_results.get("score"),
                "crack_times_seconds": zxcvbn_results.get("crack_times_seconds"),
                "crack_times_display": zxcvbn_results.get("crack_times_display"),
                "feedback": zxcvbn_results.get("feedback", {}),
                "match_sequence": zxcvbn_results.get("sequence", []),
            },
            "character_set_analysis": {
                "char_sets_used": char_sets_used,
                "char_set_size": charset_size,
            },
            "pwned_password_check": {
                "pwned": pwned_count > 0,
                "pwned_count": (
                    "Not checked"
                    if pwned_count == -2
                    else (pwned_count if pwned_count != -1 else "Error checking")
                ),
            },
            "performance": {
                "calculation_time_ms": round(calc_time_ms, 2),
            },
            "strength": get_strength_from_score(zxcvbn_results.get("score", 0)),
            "details": [],
        }

        # Format details for UI
        report["details"].append(
            {"title": "Length", "explanation": f"{len(password)} characters"}
        )
        report["details"].append(
            {
                "title": "Character Variety",
                "explanation": f"Uses: {', '.join(char_sets_used) if char_sets_used else 'None'}",
            }
        )

        if "offline_fast_hashing" in crack_time_estimates:
            report["details"].append(
                {
                    "title": "Time to Crack (Offline, Fast Hashing)",
                    "explanation": crack_time_estimates["offline_fast_hashing"][
                        "display"
                    ],
                }
            )

        if isinstance(pwned_count, int) and pwned_count > 0:
            report["details"].append(
                {
                    "title": "Pwned Status",
                    "explanation": f"Found {pwned_count} times in breaches.",
                }
            )
        elif pwned_count == 0:
            report["details"].append(
                {"title": "Pwned Status", "explanation": "Not found in breaches."}
            )

        complexity_items = [
            f"{'✅' if passed else '❌'} {req.replace('_', ' ').title()}"
            for req, passed in complexity.items()
        ]
        report["details"].append(
            {
                "title": "Complexity Requirements",
                "explanation": ", ".join(complexity_items),
            }
        )

        if zxcvbn_results.get("feedback") and zxcvbn_results["feedback"].get(
            "suggestions"
        ):
            report["details"].append(
                {
                    "title": "Suggestions",
                    "explanation": " ".join(zxcvbn_results["feedback"]["suggestions"]),
                }
            )

        return report
