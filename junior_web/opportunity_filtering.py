from general_functions import *
import datetime


def is_conviction_match(criterion, convictionRestrictions, convictionThreshold):
    maxConvictionYear = ((datetime.date.today().year - convictionThreshold)
        if convictionThreshold else datetime.date.min.year)
    return ((criterion["year"] <= maxConvictionYear) or
        (criterion["type"] not in convictionRestrictions))



def is_part_time_match(partTimeOnly, partTimeAvailable):
    return (not partTimeOnly) or partTimeAvailable


def is_drivers_license_match(hasDriversLicense, driversLicenseRequired):
    return hasDriversLicense or not driversLicenseRequired


def is_industry_match(industries, industry):
    return industry in industries


def is_abilities_match(abilities, requiredAbilities):
    return all(map(lambda r: r in abilities, requiredAbilities))


def is_opportunity_match(criteria, opportunity):
    return (
        all(map(
            lambda c: is_conviction_match(c, opportunity["convictionRestrictions"], opportunity["convictionThreshold"]),
            criteria["convictions"])) and
        is_part_time_match(criteria["partTimeOnly"], opportunity["partTimeAvailable"]) and
        is_drivers_license_match(criteria["hasDriversLicense"], opportunity["driversLicenseRequired"]) and
        is_industry_match(criteria["industries"], opportunity["industry"]) and
        is_abilities_match(criteria["abilities"], opportunity["requiredAbilities"])
    )


def filter_opportunities(criteria, opportunities):
    return filter(
        lambda o: is_opportunity_match(criteria, o),
        opportunities)
