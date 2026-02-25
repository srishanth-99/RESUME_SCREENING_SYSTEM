from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Resume Screening API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response model
class AnalysisResponse(BaseModel):
    filename: str
    content_length: int
    status: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Resume Screening API is running"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(file: UploadFile = File(...)):
    """Analyze uploaded resume file"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Validate file type (optional)
        allowed_types = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"File type not allowed. Accepted: {', '.join(allowed_types)}")
        
        content = await file.read()
        
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        logger.info(f"Successfully processed file: {file.filename}")
        
        return {
            "filename": file.filename,
            "content_length": len(content),
            "status": "success"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing file")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
