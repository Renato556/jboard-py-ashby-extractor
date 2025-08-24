class NormalizedJob:
    def __init__(self, id: str, title: str, updated_at: str, employment_type: str, published_date: str, application_deadline: str,
                 compensation_tier_summary: str | None, is_remote: bool | None, office_location: str | None, is_brazilian_friendly: dict,
                 company: str, url: str, seniority_level: str, field: str):
        self.id = id
        self.title = title
        self.updated_at = updated_at # greenhouse, lever
        self.employment_type = employment_type # greenhouse, lever
        self.published_date = published_date # greenhouse, lever
        self.deadline = application_deadline # greenhouse, lever
        self.compensation = compensation_tier_summary # greenhouse, lever
        self.is_remote = is_remote
        self.office_location = office_location
        self.is_brazilian_friendly = is_brazilian_friendly
        self.company = company
        self.url = url
        self.seniority_level = seniority_level
        self.field = field
