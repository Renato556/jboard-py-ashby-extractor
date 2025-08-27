class NormalizedJob:
    def __init__(self, title: str, updated_at: str | None, employment_type: str | None, published_date: str | None, application_deadline: str | None,
                 compensation_tier_summary: str | None, workplace_type: str | None, office_location: str | None, is_brazilian_friendly: dict,
                 company: str, url: str, seniority_level: str | None, field: str | None):
        self.title = title
        self.updated_at = updated_at # greenhouse, lever
        self.employment_type = employment_type # greenhouse, lever
        self.published_date = published_date # greenhouse, lever
        self.deadline = application_deadline # greenhouse, lever
        self.compensation = compensation_tier_summary # greenhouse, lever
        self.workplace_type = workplace_type
        self.office_location = office_location
        self.is_brazilian_friendly = is_brazilian_friendly
        self.company = company
        self.url = url
        self.seniority_level = seniority_level
        self.field = field


    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'updatedAt': self.updated_at,
            'employmentType': self.employment_type,
            'publishedDate': self.published_date,
            'applicationDeadline': self.deadline,
            'compensationTierSummary': self.compensation,
            'workplaceType': self.workplace_type,
            'officeLocation': self.office_location,
            'isBrazilianFriendly': self.is_brazilian_friendly,
            'company': self.company,
            'url': self.url,
            'seniorityLevel': self.seniority_level,
            'field': self.field
        }
