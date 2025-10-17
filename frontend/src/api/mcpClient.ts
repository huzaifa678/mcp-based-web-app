import axios from "axios";

const MCP_SERVER_URL = "/api"; 

export interface FeedbackItem {
  type: string;
  message: string;
}

export interface AnalysisResponse {
  static?: FeedbackItem[];
  ai?: FeedbackItem[];
}

/**
 * Sends code to the MCP server analyze tool and returns feedback.
 * @param code - Python code string
 */
export const analyzeCode = async (code: string, accessToken: string | null): Promise<AnalysisResponse> => {

  if (!accessToken) {
    throw new Error("No access token provided");
  }

  try {
    const response = await axios.post(`${MCP_SERVER_URL}/analyze`, { code }, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    return response.data;
    
  } catch (error: any) {
    console.error("MCP Client error:", error);
    return { ai: [{ type: "error", message: "Failed to analyze code" }] };
  }
};
