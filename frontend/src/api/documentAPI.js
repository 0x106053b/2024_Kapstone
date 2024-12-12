import documentInstance from "./documentInstance";
import { API_DOCUMENT } from "@/constants/API";

export const postUploadDocument = (chatroom_id, files) => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append("files", file);
  });

  return documentInstance({
    url: API_DOCUMENT.UPLOAD_DOCUMENT(chatroom_id),
    method: "POST",
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

export const getDocuments = (chatroom_id) => {
  return documentInstance({
    url: API_DOCUMENT.GET_DOCUMENTS(chatroom_id),
    method: "GET",
  });
};

/* response
[
  {
    "document_id": 0,
    "document_name": "string",
    "uploaded_time": "2024-11-30T15:35:46.052Z"
  }
]
*/

export const deleteDocument = (chatroom_id, document_id) => {
  return documentInstance({
    url: API_DOCUMENT.DELETE_DOCUMENT(chatroom_id, document_id),
    method: "DELETE",
  });
};
