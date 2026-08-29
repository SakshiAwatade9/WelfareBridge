"""
Rule-based eligibility engine.

Mirrors the PRD's logic:
  IF age >= minimum_age AND income <= maximum_income AND state = required_state
  AND occupation = required_occupation THEN eligible

Deterministic and explainable: every criterion that applies to a scheme is checked
individually, and the match percentage is passed/total criteria.
"""


def evaluate_scheme(profile, scheme):
    """
    profile: UserProfile model instance
    scheme: Scheme model instance
    Returns a dict with status, matchPercent, criteria breakdown, and a plain-language explanation.
    """
    criteria = []

    if scheme.min_age is not None:
        criteria.append({
            "label": f"Minimum age of {scheme.min_age} years",
            "pass": profile.age is not None and profile.age >= scheme.min_age,
        })
    if scheme.max_age is not None:
        criteria.append({
            "label": f"Maximum age of {scheme.max_age} years",
            "pass": profile.age is not None and profile.age <= scheme.max_age,
        })
    if scheme.max_income is not None:
        criteria.append({
            "label": f"Annual family income within Rs. {scheme.max_income}",
            "pass": profile.income is not None and profile.income <= scheme.max_income,
        })
    if scheme.state and scheme.state.lower() != "all india":
        criteria.append({
            "label": f"Resident of {scheme.state}",
            "pass": (profile.state or "").lower() == scheme.state.lower(),
        })
    if scheme.occupation and scheme.occupation.lower() != "any":
        criteria.append({
            "label": f"Occupation recorded as {scheme.occupation}",
            "pass": (profile.occupation or "").lower() == scheme.occupation.lower(),
        })
    if scheme.gender and scheme.gender.lower() != "any":
        criteria.append({
            "label": f"Applicant gender: {scheme.gender}",
            "pass": (profile.gender or "").lower() == scheme.gender.lower(),
        })
    if scheme.senior_only:
        criteria.append({
            "label": "Senior citizen (age 60 or above)",
            "pass": profile.age is not None and profile.age >= 60,
        })

    total = len(criteria)
    passed = sum(1 for c in criteria if c["pass"])
    match_percent = 100 if total == 0 else round((passed / total) * 100)

    if total == 0 or passed == total:
        status = "Eligible"
    elif passed >= (total + 1) // 2:  # ceil(total * 0.5)
        status = "Maybe Eligible"
    else:
        status = "Not Eligible"

    explanation = _build_explanation(status, passed, total)

    result = scheme.to_dict()
    result.update({
        "status": status,
        "matchPercent": match_percent,
        "passedCriteria": passed,
        "totalCriteria": total,
        "criteria": criteria,
        "explanation": explanation,
    })
    return result


def _build_explanation(status, passed, total):
    if total == 0:
        return "This scheme has no specific age, income, or occupation restrictions, so it applies to you."
    if status == "Eligible":
        return (f"You are eligible because your profile satisfies all {total} criteria for this scheme, "
                f"including income and category requirements where applicable.")
    if status == "Maybe Eligible":
        return (f"Your profile satisfies {passed} of {total} criteria. You may still qualify - review the "
                f"unmet criteria, as some conditions may be verified differently at the application stage.")
    return (f"Your profile satisfies only {passed} of {total} required criteria for this scheme, so it is "
            f"unlikely you qualify based on the information provided.")
