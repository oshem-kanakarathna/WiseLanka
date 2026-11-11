# A1 – WiseLanka Regulatory and Qualifications Ecosystem

## Version

0.1 – Verified Research Baseline

## Purpose

This document defines the major regulatory authorities, qualification frameworks,
recognition mechanisms and verification rules that WiseLanka must understand
before making education and career recommendations.

WiseLanka must not treat all education programmes as simply "UGC recognised"
or "not recognised". Different education sectors are governed by different
authorities and recognition mechanisms.

---

## 1. Higher Education

### University Grants Commission (UGC)

The University Grants Commission is a central authority within Sri Lanka's
higher-education system.

The state university system operates under the Universities Act No. 16 of 1978,
as amended. The Universities Act has subsequently been amended, including by the
Universities (Amendment) Act No. 2 of 2026.

WiseLanka must therefore store higher-education legislation and recognition
information in a version-aware manner.

### Sri Lanka Qualifications Framework (SLQF)

The Sri Lanka Qualifications Framework provides a nationally consistent framework
for higher-education qualifications offered in Sri Lanka.

The SLQF:

- contains twelve qualification levels
- defines learning outcomes
- defines minimum admission requirements
- identifies progression opportunities
- supports credit transfer
- supports recognition of prior learning
- links higher education with the National Vocational Qualifications Framework

WiseLanka must distinguish between:

- qualification level
- institution recognition
- programme approval
- professional recognition
- quality assurance

These concepts are related but are not equivalent.

---

## 2. Technical and Vocational Education

### Tertiary and Vocational Education Commission (TVEC)

TVEC is the principal regulatory authority for Sri Lanka's technical and vocational
education and training sector.

WiseLanka must distinguish between:

- a registered training provider
- an accredited programme
- an NVQ qualification
- the validity period of accreditation

A provider being registered does not automatically mean that every programme it
offers is accredited.

### National Vocational Qualifications Framework

The NVQ framework represents occupational and vocational qualifications and
provides progression pathways through different levels.

WiseLanka should represent NVQ qualifications separately from SLQF qualifications
while supporting evidence-based progression links between them.

---

## 3. General Education

### Department of Examinations Sri Lanka

The Department of Examinations is responsible for national examinations including:

- GCE Ordinary Level
- GCE Advanced Level
- Grade 5 Scholarship Examination
- other institutional and professional examinations administered by the Department

The Department also provides:

- official examination results
- certificates
- result verification
- examination information

WiseLanka should treat Department of Examinations records as authoritative sources
for national examination qualifications.

---

## 4. Recognition Model

WiseLanka must not use a single Boolean field such as:

is_recognised = true / false

Instead, recognition should record:

- recognised by whom
- recognition type
- qualification or programme concerned
- effective date
- expiry date where applicable
- delivery location
- professional recognition where relevant
- evidence source
- last verification date
- confidence level

---

## 5. Recognition Vocabulary

WiseLanka should distinguish the following terms:

### Registered
The provider or institution appears on an applicable official register.

### Approved
An authority has formally authorised a programme or activity.

### Accredited
A competent authority has assessed a programme or provider against defined
standards.

### Recognised
An authority accepts a qualification or institution for a defined purpose.

### Framework-Aligned
A qualification is positioned within a recognised qualifications framework.

### Professionally Recognised
A professional body accepts the programme or qualification for a particular
professional purpose.

### Verified
WiseLanka has checked the claim against an authoritative source.

---

## 6. Evidence Hierarchy

Recognition-related claims should prioritise evidence in the following order:

1. Acts of Parliament and amendments
2. Gazette notifications
3. Official regulator databases
4. Official recognition or accreditation records
5. Official university or awarding-body publications
6. Official programme documentation
7. Reputable secondary sources where primary evidence is unavailable

Provider advertising alone must not be treated as proof of recognition.

---

## 7. WiseLanka Policy Rule

Before recommending a programme, WiseLanka should:

1. identify the awarding organisation
2. identify the teaching organisation
3. verify the applicable regulatory domain
4. determine qualification level
5. check programme or provider recognition where applicable
6. check learner eligibility
7. identify professional requirements where relevant
8. attach supporting evidence
9. show uncertainty where evidence is incomplete

---

## 8. Current Core Authorities

Initial authorities to model include:

- University Grants Commission
- Quality Assurance Council
- Tertiary and Vocational Education Commission
- Department of Examinations Sri Lanka
- Ministry of Education
- National Institute of Education
- profession-specific regulatory bodies

This list will be expanded during later research phases.

---

## 9. Core Design Conclusion

WiseLanka must operate as a multi-authority, evidence-based education intelligence
platform.

The correct question is not simply:

"Is this recognised?"

The correct questions are:

- Recognised by whom?
- For what purpose?
- For which programme or qualification?
- During which period?
- Under which official evidence?
- Does professional practice require additional recognition?