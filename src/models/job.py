class Job:
    def __init__(self, id: str, title: str, updatedAt: str, suppressDescriptionOpening: bool, suppressDescriptionClosing: bool, departmentId: str, departmentName: str,
                 locationId: str, locationName: str, workplaceType: str, employmentType: str, isListed: bool, jobId: str, jobRequisitionId: str, teamId: str, teamName: str,
                 publishedDate: str, applicationDeadline: str, shouldDisplayCompensationOnJobBoard: str, secondaryLocations: list, compensationTierSummary: str, userRoles: list):
        self.id = id
        self.title = title
        self.updatedAt = updatedAt
        self.suppressDescriptionOpening = suppressDescriptionOpening
        self.suppressDescriptionClosing = suppressDescriptionClosing
        self.departmentId = departmentId
        self.departmentName = departmentName
        self.locationId = locationId
        self.locationName = locationName
        self.workplaceType = workplaceType
        self.employmentType = employmentType
        self.isListed = isListed
        self.jobId = jobId
        self.jobRequisitionId = jobRequisitionId
        self.teamId = teamId
        self.teamName = teamName
        self.publishedDate = publishedDate
        self.applicationDeadline = applicationDeadline
        self.shouldDisplayCompensationOnJobBoard = shouldDisplayCompensationOnJobBoard
        self.secondaryLocations = secondaryLocations
        self.compensationTierSummary = compensationTierSummary
        self.userRoles = userRoles