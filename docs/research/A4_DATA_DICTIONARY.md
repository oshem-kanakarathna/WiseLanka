# A4 – WiseLanka Data Dictionary

## Version

0.1 Draft

## Purpose

This document defines the structure, meaning, validation rules and relationships of the core WiseLanka datasets.

The initial data model is designed to support a focused interim demonstration while remaining extensible enough to add additional institutions, qualifications, programmes, careers, scholarships, skills and policy records without redesigning the system.

## Identifier Standard

WiseLanka uses stable identifiers for core entities.

Examples:

- Institution: INS0001
- Qualification: QLF0001
- Programme: PRG0001
- Career: CAR0001
- Skill: SKL0001
- Scholarship: SCH0001
- Recognition Record: REC0001
- Evidence Source: SRC0001

Identifiers should remain stable even if display names change.

## Dataset: Institutions

### Purpose

The Institutions dataset stores education providers, awarding organisations, regulatory-linked institutions and other recognised learning providers referenced by WiseLanka.

### Fields

| Field | Type | Required | Description | Example |
|---|---|---:|---|---|
| institution_id | String | Yes | Stable unique identifier | INS0001 |
| institution_name | Text | Yes | Official institution name | University of Colombo |
| institution_type | Enum/String | Yes | Type of institution | State University |
| ownership_type | Enum/String | Yes | Ownership category | Government |
| awarding_authority | Boolean | Yes | Whether institution can award qualifications directly | true |
| country | Text | Yes | Country where institution is based | Sri Lanka |
| province | Text | No | Province of main campus | Western |
| district | Text | No | District of main campus | Colombo |
| city | Text | No | Main city/location | Colombo |
| official_website | URL | No | Official institution website | https://... |
| active_status | Enum/String | Yes | Current operating status | Active |
| notes | Text | No | Additional contextual information | Main state university |

### Validation Rules

- `institution_id` must be unique.
- `institution_name` cannot be empty.
- `institution_type` must come from the controlled institution type list.
- `country` cannot be empty.
- `active_status` should use controlled values such as `Active`, `Inactive`, `Suspended`, or `Archived`.
- Recognition must not be stored as a simple yes/no field inside this dataset.
- Recognition details must be stored separately in the Recognition Records dataset.

### Relationships

An institution may:

- offer many programmes
- award many qualifications
- operate multiple campuses
- have multiple recognition records
- provide scholarships
- act as a teaching centre for another awarding institution

## Dataset: Qualifications

### Purpose

The Qualifications dataset stores recognised academic, vocational, professional and school-level qualifications that may be held, pursued or awarded within education and career pathways represented by WiseLanka.

Qualifications are stored separately from programmes because the same qualification type may be awarded through different programmes and institutions.

### Fields

| Field | Type | Required | Description | Example |
|---|---|---:|---|---|
| qualification_id | String | Yes | Stable unique qualification identifier | QLF0001 |
| qualification_name | Text | Yes | Official or canonical qualification name | GCE Advanced Level |
| qualification_type | Enum/String | Yes | General qualification category | School Qualification |
| framework_name | Text | No | Framework associated with qualification | SLQF |
| framework_level | String/Integer | No | Level within relevant framework | 6 |
| awarding_body_id | String/FK | No | Organisation responsible for awarding qualification | INS0001 |
| education_sector | Enum/String | Yes | General education sector | Higher Education |
| field_specific | Boolean | Yes | Whether the qualification is restricted to a specific discipline | false |
| minimum_duration_months | Integer | No | Typical minimum duration where applicable | 48 |
| credit_value | Decimal/Integer | No | Credit value where officially applicable | 120 |
| country | Text | Yes | Primary national context of qualification | Sri Lanka |
| active_status | Enum/String | Yes | Current status | Active |
| notes | Text | No | Additional information | Honours undergraduate qualification |

### Example Qualification Categories

WiseLanka should be able to represent:

- GCE Ordinary Level
- GCE Advanced Level
- Cambridge O Level
- Cambridge International A Level
- Pearson Edexcel qualifications
- Foundation qualifications
- Certificates
- Advanced Certificates
- Diplomas
- Higher Diplomas
- NVQ qualifications
- Bachelor's Degrees
- Bachelor's Honours Degrees
- Postgraduate Certificates
- Postgraduate Diplomas
- Master's Degrees
- MPhil qualifications
- Doctoral qualifications
- Professional qualifications
- Industry certifications
- Short-course or microcredential awards where appropriate

### Validation Rules

- `qualification_id` must be unique.
- `qualification_name` cannot be empty.
- `qualification_type` must use a controlled list.
- Framework level must not be assumed solely from the qualification title.
- SLQF and NVQ levels must be stored with their corresponding framework.
- Recognition must not be inferred from the qualification name alone.
- Awarding body information should be linked through an organisation identifier where applicable.
- Short courses that do not belong to a formal qualifications framework must not be falsely assigned an SLQF or NVQ level.

### Relationships

A qualification may:

- be awarded by one or more authorised awarding organisations
- be produced by multiple programmes
- satisfy programme entry requirements
- provide progression to other qualifications
- have an equivalence relationship with another qualification
- belong to a qualifications framework
- have recognition or verification evidence

---

## Dataset: Programmes

### Purpose

The Programmes dataset stores structured learning opportunities available to learners.

A programme represents the actual course of study that a learner can enrol in. It is kept separate from the qualification awarded, institution offering the programme, entry requirements, recognition evidence, career outcomes and skills.

This separation allows WiseLanka to represent complex arrangements such as a Sri Lankan teaching institution delivering a programme leading to a qualification awarded by another organisation.

### Fields

| Field | Type | Required | Description | Example |
|---|---|---:|---|---|
| programme_id | String | Yes | Stable unique programme identifier | PRG0001 |
| programme_name | Text | Yes | Official programme title | BSc (Hons) Computer Science |
| programme_type | Enum/String | Yes | General programme category | Bachelor's Degree |
| provider_institution_id | String/FK | Yes | Institution delivering the programme | INS0001 |
| awarding_body_id | String/FK | No | Organisation awarding the final qualification | INS0001 |
| qualification_id | String/FK | No | Qualification produced on successful completion | QLF0001 |
| field_of_study | Text | Yes | Main academic/vocational field | Computer Science |
| specialisation | Text | No | More specific subject area | Artificial Intelligence |
| duration_months | Integer | No | Normal programme duration | 48 |
| study_mode | Enum/String | Yes | Full-time, part-time, etc. | Full-time |
| delivery_mode | Enum/String | Yes | Physical, online or hybrid delivery | Physical |
| language | Text | No | Primary language of instruction | English |
| country | Text | Yes | Country where programme is offered | Sri Lanka |
| province | Text | No | Province of delivery | Western |
| district | Text | No | District of delivery | Colombo |
| campus | Text | No | Campus or teaching location | Main Campus |
| total_fee_lkr | Decimal | No | Published approximate total tuition fee in LKR | 1200000 |
| application_fee_lkr | Decimal | No | Application fee where applicable | 5000 |
| currency | String | No | Original fee currency | LKR |
| intake_information | Text | No | General intake information | September |
| application_url | URL | No | Official application/programme page | https://... |
| programme_status | Enum/String | Yes | Current programme status | Active |
| last_verified_date | Date | No | Most recent WiseLanka verification date | 2026-08-07 |
| notes | Text | No | Additional programme information | Weekend option available |

### Important Modelling Rules

The following information must NOT be permanently embedded as free-text inside the programme record when it represents a separate relationship:

- detailed entry requirements
- career outcomes
- required or developed skills
- scholarships
- recognition/accreditation evidence
- progression pathways

These are represented using relationship datasets.

For example:

Programme → Entry Requirement

Programme → Career

Programme → Skill

Programme → Recognition Record

Programme → Scholarship

This avoids duplicated information and allows relationships to be updated independently.

### Provider vs Awarding Body

WiseLanka must distinguish between the organisation that teaches a programme and the organisation that awards the qualification.

For example:

Teaching Provider
        ↓
Programme
        ↓
Awarding Organisation
        ↓
Qualification

The provider and awarding organisation may be the same institution, but WiseLanka must not assume that they are always identical.

### Fee Modelling

Programme cost information is time-sensitive.

The initial demonstration may store a recently verified approximate fee in the programme record for filtering and recommendation purposes.

A future version should maintain a separate fee-history dataset containing:

- programme
- intake
- fee type
- amount
- currency
- effective date
- evidence source

This prevents historical fee information from being overwritten.

### Validation Rules

- `programme_id` must be unique.
- `programme_name` cannot be empty.
- `provider_institution_id` must reference an existing institution.
- `qualification_id`, when supplied, must reference an existing qualification.
- `awarding_body_id`, when supplied, must reference an existing organisation.
- `duration_months` cannot be negative.
- monetary values cannot be negative.
- `programme_status` must use controlled values.
- recognition must not be inferred from institution reputation or programme title.
- programme fees must include a verification date when used for recommendations.
- missing information must remain unknown rather than being guessed.

### Relationships

A programme may:

- be offered by an institution
- lead to a qualification
- have an external awarding organisation
- have multiple entry requirements
- lead towards multiple careers
- develop multiple skills
- have multiple recognition records
- qualify for multiple scholarships
- provide progression to further study
- have multiple delivery locations
- have multiple intakes
- have multiple evidence sources

## Dataset: Careers

### Purpose

The Careers dataset stores occupations and professional destinations that learners may pursue through education, training, skills development and professional progression.

Career records are maintained separately from programmes because a single programme may lead towards multiple careers, while the same career may be accessible through multiple educational pathways.

### Fields

| Field | Type | Required | Description | Example |
|---|---|---:|---|---|
| career_id | String | Yes | Stable unique career identifier | CAR0001 |
| career_name | Text | Yes | Canonical career or occupation name | Software Engineer |
| career_category | Enum/String | Yes | Broad occupational category | Software Development |
| industry | Text | No | Primary associated industry | Information Technology |
| description | Text | Yes | Short description of the career | Designs develops tests and maintains software systems |
| minimum_qualification_level | Text | No | Typical minimum qualification level where evidence supports one | Bachelor's Degree |
| sri_lanka_demand | Enum/String | No | Evidence-supported indication of demand within Sri Lanka | High |
| international_potential | Enum/String | No | Indicative international career potential | High |
| remote_work_potential | Enum/String | No | Indicative potential for remote employment | High |
| self_employment_potential | Enum/String | No | Indicative potential for freelance or self-employed work | Medium |
| active_status | Enum/String | Yes | Whether the career record is active | Active |
| notes | Text | No | Additional contextual or evidence notes | Demand classification requires supporting evidence |

### Controlled Values

Where classification values are available, the following controlled scale should be used:

- `High`
- `Medium`
- `Low`
- `Unknown`

`Unknown` should be used when WiseLanka does not yet have sufficient evidence to assign a reliable classification.

Missing evidence must not automatically be interpreted as `Low`.

### Validation Rules

- `career_id` must be unique.
- `career_name` cannot be empty.
- `career_category` cannot be empty.
- `active_status` should use controlled values such as `Active`, `Inactive`, or `Archived`.
- Demand and potential classifications must use controlled values.
- Career demand must not be inferred solely from programme availability.
- `sri_lanka_demand` should be supported by appropriate labour-market, government, industry or employment evidence.
- International and remote-work potential should not be presented as guaranteed employment outcomes.
- Where sufficient evidence is unavailable, the relevant classification should remain `Unknown`.

### Evidence and Explainability

Career indicators should be traceable to evidence wherever possible.

Examples of suitable evidence include:

- government labour-market publications
- national workforce surveys
- recognised industry reports
- official occupational information
- reputable employment-market datasets

The recommendation layer should distinguish between verified facts, evidence-supported indicators and future predictive outputs.

### Relationships

A career may:

- be associated with many programmes
- require or benefit from many skills
- be accessible through multiple qualifications
- belong to one or more industry areas
- have multiple supporting evidence sources

Programme-to-career relationships must be stored separately rather than embedded directly inside programme records.

Example:

Programme
    ↓
Programme-Career Relationship
    ↓
Career