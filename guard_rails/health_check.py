"""
LLM Health Check - Identifies Python files that need optimization based on line count.

Health Score Calculation:
- Files <= 100 lines: 100% health
- Every 100 lines over the threshold: -10% health
- Minimum health: 0%
"""

import os
from pathlib import Path


def calculate_health(line_count: int, threshold: int = 100) -> int:
    if line_count <= threshold:
        return 100
    excess = line_count - threshold
    penalty = (excess // 100) * 10 + (10 if excess % 100 > 0 else 0)
    return max(0, 100 - penalty)


def scan_python_files(directory: str) -> list[dict]:
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".py"):
                continue
            filepath = Path(root) / file
            if "migrations" in str(filepath) or "__pycache__" in str(filepath):
                continue
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    code_lines = sum(
                        1 for line in lines
                        if line.strip() and not line.strip().startswith("#")
                    )
                    total_lines = len(lines)
            except Exception:
                continue
            results.append({
                "path": str(filepath),
                "total_lines": total_lines,
                "code_lines": code_lines,
                "health": calculate_health(code_lines),
            })
    return results


def main():
    results = scan_python_files("apps")
    results.sort(key=lambda x: (x["health"], -x["code_lines"]))
    worst_10 = results[:10]

    print("LLM HEALTH CHECK - TOP 10 FILES NEEDING OPTIMIZATION")
    print()
    for i, item in enumerate(worst_10, 1):
        print(f"{i}. {item['path']}")
        print(f"   health: {item['health']}%, code_lines: {item['code_lines']}, total_lines: {item['total_lines']}")
        print()

    total_files = len(results)
    healthy = sum(1 for r in results if r["health"] >= 80)
    warning = sum(1 for r in results if 40 <= r["health"] < 80)
    critical = sum(1 for r in results if r["health"] < 40)
    avg_health = sum(r["health"] for r in results) / total_files if total_files else 0

    print("SUMMARY")
    print(f"total_files: {total_files}")
    print(f"avg_health: {avg_health:.1f}%")
    print(f"healthy (80%+): {healthy}")
    print(f"warning (40-79%): {warning}")
    print(f"critical (<40%): {critical}")


if __name__ == "__main__":
    main()
