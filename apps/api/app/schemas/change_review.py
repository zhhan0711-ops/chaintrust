from pydantic import BaseModel
class ChangeReviewRequest(BaseModel):
    baseline_source:str=''; candidate_source:str=''; deployed_address:str|None=None; sandbox:bool=False