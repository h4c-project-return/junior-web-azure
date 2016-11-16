from general_functions import *

KNOWN_HEADERS = {
    "name": "Company Name",
    "convictionThreshold": "Conviction Threshold (Yrs)",
    "convictionRestrictions": "Conviction Restrictions",
    "schedule": "Part Time / Full Time",
    "industry": "Industry",
    "type": "Type",
    "requiredAbilities": "Required Abilities",
    "driversLicenseRequired": "Requires Driver's License",
}


def parse_headers(sheet_values):
    return zip_padded(
        fill_none(strip_all(sheet_values[0])),
        strip_all(sheet_values[1]),
        "")


def get_opportunities_criteria(sheet_values):
    criteria = {
        "abilities": [],
        "convictions": [],
        "industries": []
    }
    tempconv = {}
    tempabilities = {}

    for i, v in enumerate(parse_headers(sheet_values)):
        if "Conviction" in v[0]:
            if v[1]:
                tempconv[v[1]] = ''
            else:
                pass
        elif "Abilities" in v[0]:
            if v[1]:
                tempabilities[v[1]] = ''
            else:
                pass
        else:
            industries = list((distinct(map(
                lambda d: d["industry"],
                parse_opportunities(sheet_values)))))

    criteria['abilities'] = tempabilities
    criteria['convictions'] = tempconv
    criteria['industries'] = industries

    return criteria


def parse_value_single(primary_header, sheet_row, sheet_headers):
    pairs = parse_value_pairs(primary_header, id, sheet_row, sheet_headers)
    if len(pairs) > 1:
        raise Exception("Expected one item; found more.")
    return pairs[0][1]


def parse_value_pairs(primary_header, parser, sheet_row, sheet_headers):
    header_value_pairs = zip_padded(sheet_headers, sheet_row, "")
    return map(
        lambda (hdr, value): (hdr[1], parser(value.strip())),
        filter(
            lambda item: item[0][0] == primary_header,
            header_value_pairs))


def parse_value_single_or_pairs(primary_header, list_proc, sheet_row, sheet_headers):
    pairs = parse_value_pairs(primary_header, id, sheet_row, sheet_headers)
    return list_proc(pairs) if len(pairs) > 1 else pairs[0][1]


def parse_boolean(s):
    return s.lower() == "true"


def parse_int_maybe(s):
    return None if s == "" else int(s)


def parse_opportunity(sheet_row, sheet_headers):
    return {
        "name":
            parse_value_single(KNOWN_HEADERS["name"], sheet_row, sheet_headers),
        "convictionThreshold":
            parse_int_maybe(parse_value_single(KNOWN_HEADERS["convictionThreshold"], sheet_row, sheet_headers)),
        "convictionRestrictions":
            map(lambda pair: pair[0], filter(lambda pair: pair[1],
                                             parse_value_pairs(KNOWN_HEADERS["convictionRestrictions"], parse_boolean,
                                                               sheet_row, sheet_headers))),
        "partTimeAvailable":
            "PT" in parse_value_single(KNOWN_HEADERS["schedule"], sheet_row, sheet_headers),
        "industry":
            parse_value_single(KNOWN_HEADERS["industry"], sheet_row, sheet_headers),
        "type":
            parse_value_single(KNOWN_HEADERS["type"], sheet_row, sheet_headers),
        "schedule":
            parse_value_single(KNOWN_HEADERS["schedule"], sheet_row, sheet_headers),
        "requiredAbilities":
            map(lambda pair: pair[0], filter(lambda pair: pair[1],
                                             parse_value_pairs(KNOWN_HEADERS["requiredAbilities"], parse_boolean,
                                                               sheet_row, sheet_headers))),
        "driversLicenseRequired":
            parse_boolean(parse_value_single(KNOWN_HEADERS["driversLicenseRequired"], sheet_row, sheet_headers)),
        "humanFriendly":
            key_val_dict_list(
                map(
                    lambda hdr: (
                        hdr,
                        parse_value_single_or_pairs(hdr, key_val_dict_list, sheet_row, sheet_headers)),
                    filter(
                        lambda hdr: hdr not in KNOWN_HEADERS.values(),
                        distinct(map(lambda hdr_pair: hdr_pair[0], sheet_headers))))),
    }


def parse_opportunities(sheet_values):
    return map(
        lambda row: parse_opportunity(row, parse_headers(sheet_values)),
        filter(lambda row: row[0].strip() != "", skip(2, sheet_values)))
