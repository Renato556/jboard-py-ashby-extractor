from src.models.job import Job


class FriendlyJob(Job):
    def __init__(self, job: Job, is_brazilian_friendly: dict | None):
        super().__init__(
            id=getattr(job, 'id', None),
            title=getattr(job, 'title', None),
            updatedAt=getattr(job, 'updatedAt', None),
            suppressDescriptionOpening=getattr(job, 'suppressDescriptionOpening', None),
            suppressDescriptionClosing=getattr(job, 'suppressDescriptionClosing', None),
            departmentId=getattr(job, 'departmentId', None),
            departmentName=getattr(job, 'departmentName', None),
            locationId=getattr(job, 'locationId', None),
            locationName=getattr(job, 'locationName', None),
            workplaceType=getattr(job, 'workplaceType', None),
            employmentType=getattr(job, 'employmentType', None),
            isListed=getattr(job, 'isListed', None),
            jobId=getattr(job, 'jobId', None),
            jobRequisitionId=getattr(job, 'jobRequisitionId', None),
            teamId=getattr(job, 'teamId', None),
            teamName=getattr(job, 'teamName', None),
            publishedDate=getattr(job, 'publishedDate', None),
            applicationDeadline=getattr(job, 'applicationDeadline', None),
            shouldDisplayCompensationOnJobBoard=getattr(job, 'shouldDisplayCompensationOnJobBoard', None),
            secondaryLocations=getattr(job, 'secondaryLocations', None),
            compensationTierSummary=getattr(job, 'compensationTierSummary', None),
            userRoles=getattr(job, 'userRoles', None),
        )
        self.is_brazilian_friendly = is_brazilian_friendly


    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'updatedAt': self.updatedAt,
            'suppressDescriptionOpening': self.suppressDescriptionOpening,
            'suppressDescriptionClosing': self.suppressDescriptionClosing,
            'departmentId': self.departmentId,
            'departmentName': self.departmentName,
            'locationId': self.locationId,
            'locationName': self.locationName,
            'workplaceType': self.workplaceType,
            'employmentType': self.employmentType,
            'isListed': self.isListed,
            'jobId': self.jobId,
            'jobRequisitionId': self.jobRequisitionId,
            'teamId': self.teamId,
            'teamName': self.teamName,
            'publishedDate': self.publishedDate,
            'applicationDeadline': self.applicationDeadline,
            'shouldDisplayCompensationOnJobBoard': self.shouldDisplayCompensationOnJobBoard,
            'secondaryLocations': self.secondaryLocations,
            'compensationTierSummary': self.compensationTierSummary,
            'userRoles': self.userRoles,
            'is_brazilian_friendly': self.is_brazilian_friendly
        }