"""Validate identifiers and relationships before serving educational guidance."""
from backend.app.data_loader import load_csv, KnowledgeDataError

TABLES = {
    'institution_types': ('master/institution_types.csv', 'institution_type_id'),
    'programme_types': ('master/programme_types.csv', 'programme_type_id'),
    'qualification_frameworks': ('master/qualification_frameworks.csv', 'framework_id'),
    'qualification_types': ('master/qualification_types.csv', 'qualification_type_id'),
    'study_modes': ('master/study_modes.csv', 'study_mode_id'),
    'institutions': ('reference/institutions.csv', 'institution_id'),
    'qualifications': ('reference/qualifications.csv', 'qualification_id'),
    'programmes': ('reference/programmes.csv', 'programme_id'),
    'careers': ('reference/careers.csv', 'career_id'),
    'skills': ('reference/skills.csv', 'skill_id'),
    'scholarships': ('reference/scholarships.csv', 'scholarship_id'),
    'sources': ('metadata/evidence_sources.csv', 'source_id'),
    'recognition': ('metadata/recognition_records.csv', 'recognition_id'),
    'requirements': ('relationships/programme_entry_requirements.csv', 'requirement_id'),
    'progression': ('relationships/qualification_progression.csv', 'progression_id'),
    'programme_careers': ('relationships/programme_careers.csv', None),
    'programme_skills': ('relationships/programme_skills.csv', None),
    'career_skills': ('relationships/career_skills.csv', None),
    'scholarship_requirements': ('relationships/scholarship_eligibility_requirements.csv', 'requirement_id'),
    'scholarship_applicability': ('relationships/scholarship_applicability.csv', 'applicability_id'),
}


def validate_catalogue():
    tables = {name: load_csv(path) for name, (path, _) in TABLES.items()}
    errors = []
    ids = {}
    for name, rows in tables.items():
        key = TABLES[name][1]
        values = [row.get(key, '') for row in rows] if key else []
        if key and (any(not value for value in values) or len(values) != len(set(values))):
            errors.append(f'{name}: missing or duplicate {key}')
        ids[name] = set(values)
        signatures = [tuple(sorted(row.items())) for row in rows]
        if len(signatures) != len(set(signatures)):
            errors.append(f'{name}: duplicate relationship/record')

    def references(table, field, target, optional=False):
        for row in tables[table]:
            value = row.get(field, '')
            if optional and not value:
                continue
            if value not in ids[target]:
                errors.append(f'{table}.{field}: unknown {value!r}')

    for field in ('provider_institution_id', 'awarding_body_id'):
        references('programmes', field, 'institutions', optional=field == 'awarding_body_id')
    references('programmes', 'qualification_id', 'qualifications')
    references('qualifications', 'awarding_body_id', 'institutions', optional=True)
    references('qualifications', 'source_id', 'sources', optional=True)
    references('programmes', 'source_id', 'sources')
    for table in ('requirements', 'programme_careers', 'programme_skills'):
        references(table, 'programme_id', 'programmes')
    references('requirements', 'source_id', 'sources')
    references('requirements', 'qualification_id', 'qualifications', optional=True)
    for field in ('from_qualification_id', 'to_qualification_id'):
        references('progression', field, 'qualifications')
    references('progression', 'source_id', 'sources')
    references('progression', 'supporting_source_id', 'sources', optional=True)
    references('recognition', 'source_id', 'sources')
    for row in tables['recognition']:
        target = {'Institution': 'institutions', 'Programme': 'programmes', 'Qualification': 'qualifications'}.get(row['entity_type'])
        if not target or row['entity_id'] not in ids[target]:
            errors.append('recognition: invalid entity reference')
    for table in ('programme_careers', 'career_skills'):
        references(table, 'career_id', 'careers')
    for table in ('programme_skills', 'career_skills'):
        references(table, 'skill_id', 'skills')
    for table in ('scholarship_requirements', 'scholarship_applicability'):
        references(table, 'scholarship_id', 'scholarships')
    references('scholarship_requirements', 'source_id', 'sources')
    references('scholarship_applicability', 'source_id', 'sources')
    for table, fields in (
        ('programme_careers', ('programme_id', 'career_id')),
        ('programme_skills', ('programme_id', 'skill_id')),
        ('career_skills', ('career_id', 'skill_id')),
    ):
        pairs = [tuple(row[field] for field in fields) for row in tables[table]]
        if len(pairs) != len(set(pairs)):
            errors.append(f'{table}: duplicate relationship key')
    for row in tables['programmes']:
        if row.get('domain') not in {'Information Technology', 'Business and Management', 'Engineering'}:
            errors.append('programmes: unknown approved domain')
    groups = {}
    for row in tables['requirements']:
        key = (row['programme_id'], row['requirement_group_id'])
        previous = groups.setdefault(key, row['group_operator'])
        if row['group_operator'] not in {'AND', 'OR'} or previous != row['group_operator']:
            errors.append('requirements: invalid or inconsistent group operator')
        if not row['requirement_group_id']:
            errors.append('requirements: missing group identifier')
        if row['requirement_type'] in {'A_LEVEL_PASS', 'SUBJECT_SET_COUNT', 'O_LEVEL_PASS_COUNT', 'O_LEVEL_CREDIT_COUNT'}:
            if not row['minimum_count'].isdigit() or int(row['minimum_count']) < 1:
                errors.append('requirements: invalid minimum count')
    if errors:
        raise KnowledgeDataError('; '.join(errors))
    return {name: len(rows) for name, rows in tables.items()}


if __name__ == '__main__':
    print(validate_catalogue())
