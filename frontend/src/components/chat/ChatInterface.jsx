import React, { useState, useEffect } from "react";
import { ChatSidebar } from "./ChatSideBar";
import { ChatMessages } from "./ChatMessages";
import { ChatInput } from "./ChatInput";
import { NewRoomDialog } from "./NewRoomDialog";
import FileUploadDialog from "./FileUploadDialog";
import { useNavigate } from "react-router-dom";
import { getUser } from "@/api/userAPI";
import {
  getChatrooms,
  postCreateChatroom,
  deleteChatroom,
} from "@/api/chatroomAPI";
import { getMessage, postSendMessage, deleteMessage } from "@/api/messageAPI";
import {
  getDocuments,
  postUploadDocument,
  deleteDocument,
} from "@/api/documentAPI";
import Cookies from "js-cookie";

export default function ChatInterface({ setIsLoggedIn }) {
  // 채팅방 관련 상태
  const [chatRooms, setChatRooms] = useState([]);
  const [selectedRoomId, setSelectedRoomId] = useState(null);

  // 메시지 입력 관련 상태
  const [inputMessage, setInputMessage] = useState("");

  // 새 채팅방 생성 관련 상태
  const [isNewRoomDialogOpen, setIsNewRoomDialogOpen] = useState(false);
  const [newRoomName, setNewRoomName] = useState("");
  const [newRoomInstructor, setNewRoomInstructor] = useState("");
  const [newRoomCourseCode, setNewRoomCourseCode] = useState("");

  // 파일 업로드 관련 상태
  const [isFileUploadDialogOpen, setIsFileUploadDialogOpen] = useState(false);

  // 유저 정보 상태
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const accessToken = Cookies.get("access_token");

  //chatroom들 상태 (나중에 삭제할 것)
  useEffect(() => {
    console.log("Current chat rooms state:", chatRooms);
  }, [chatRooms]);

  // 현재 선택된 채팅방 찾기
  const selectedRoom = chatRooms.find(
    (room) => room.chatroom_id === selectedRoomId
  );

  // 메시지 가져오기
  const fetchMessages = async (roomId) => {
    try {
      const response = await getMessage(roomId);
      const formattedMessages = response.data.map((message) => ({
        ...message,
      }));
      setChatRooms((prevRooms) =>
        prevRooms.map((room) =>
          room.chatroom_id === roomId
            ? { ...room, messages: formattedMessages }
            : room
        )
      );
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  //자료 가져오기
  const fetchDocuments = async (roomId) => {
    try {
      const response = await getDocuments(roomId);
      setChatRooms((prevRooms) =>
        prevRooms.map((room) =>
          room.chatroom_id === roomId ? { ...room, files: response.data } : room
        )
      );
    } catch (error) {
      console.error("Error fetching documents:", error);
    }
  };

  // 채팅방 선택 처리
  const handleRoomSelect = (roomId) => {
    setSelectedRoomId(roomId);
    fetchMessages(roomId);
    fetchDocuments(roomId);
  };

  // 유저 정보와 채팅방 목록 가져오기
  useEffect(() => {
    const fetchData = async () => {
      if (!accessToken) {
        console.log("토큰이 없습니다:", {
          accessToken: !!accessToken,
        });
        return;
      }

      try {
        const [userResponse, chatroomsResponse] = await Promise.all([
          getUser(),
          getChatrooms(),
        ]);
        setUser(userResponse.data);
        setChatRooms(
          chatroomsResponse.data.map((room) => ({
            ...room,
            messages: [],
            files: [],
          }))
        );
      } catch (error) {
        console.error("Error fetching data:", error);
        if (error.response?.status === 401) {
          navigate("/login");
        }
      }
    };

    if (accessToken) {
      fetchData();
    }
  }, []);

  // 메시지 전송 처리
  const handleSendMessage = async () => {
    if (inputMessage.trim() && selectedRoomId) {
      const newMessage = {
        message_id: Date.now(), // 임시 ID
        content: inputMessage.trim(),
        sender_type: "user",
        send_time: new Date().toISOString(),
      };

      // user가 보내는 메시지
      setChatRooms((prevRooms) =>
        prevRooms.map((room) =>
          room.chatroom_id === selectedRoomId
            ? { ...room, messages: [...room.messages, newMessage] }
            : room
        )
      );

      setInputMessage("");

      try {
        const response = await postSendMessage(
          selectedRoomId,
          newMessage.content
        );
        const serverMessage = {
          ...response.data,
        };

        //llm으로부터 받는 메시지
        setChatRooms((prevRooms) =>
          prevRooms.map((room) =>
            room.chatroom_id === selectedRoomId
              ? {
                  ...room,
                  messages: [...room.messages, serverMessage],
                }
              : room
          )
        );
      } catch (error) {
        console.error("Error sending message:", error);
      }
    }
  };

  // 새 채팅방 생성 처리
  const handleNewRoomSubmit = async () => {
    if (newRoomName) {
      try {
        const response = await postCreateChatroom(
          newRoomName,
          newRoomInstructor,
          newRoomCourseCode
        );

        const newRoom = {
          chatroom_id: response.data.chatroom_id,
          chatroom_name: newRoomName,
          instructor_name: newRoomInstructor || undefined,
          course_code: newRoomCourseCode || undefined,
          messages: [],
          files: [],
        };

        setChatRooms((prevRooms) => [...prevRooms, newRoom]);
        setIsNewRoomDialogOpen(false);
        setNewRoomName("");
        setNewRoomInstructor("");
        setNewRoomCourseCode("");
        setSelectedRoomId(newRoom.chatroom_id);
      } catch (error) {
        console.error("Error creating new room:", error);
      }
    }
  };

  // 파일 업로드 처리
  const handleFileUpload = async (files) => {
    if (selectedRoomId) {
      try {
        const response = await postUploadDocument(selectedRoomId, files);

        setChatRooms((prevRooms) =>
          prevRooms.map((room) =>
            room.chatroom_id === selectedRoomId
              ? {
                  ...room,
                  files: [...room.files, ...response.data.uploaded_files],
                }
              : room
          )
        );

        setIsFileUploadDialogOpen(false);
      } catch (error) {
        if (error.response) {
          console.error("Error details:", error.response.data);
        } else {
          console.error("Unexpected error:", error);
        }
      }
    }
  };

  // 파일 제거 처리
  const handleFileRemove = async (fileToRemove) => {
    if (selectedRoomId) {
      try {
        await deleteDocument(selectedRoomId, fileToRemove.document_id);
        setChatRooms((prevRooms) =>
          prevRooms.map((room) =>
            room.chatroom_id === selectedRoomId
              ? {
                  ...room,
                  files: room.files.filter(
                    (file) => file.document_id !== fileToRemove.document_id
                  ),
                }
              : room
          )
        );
      } catch (error) {
        console.error("Error deleting file:", error);
      }
    }
  };

  // 채팅방 삭제 처리(채팅방 내 모든 메시지도 삭제 처리)
  const handleDeleteRoom = async (roomId) => {
    try {
      await Promise.all([deleteChatroom(roomId), deleteMessage(roomId)]);
      setChatRooms((prevRooms) =>
        prevRooms.filter((room) => room.chatroom_id !== roomId)
      );
      if (selectedRoomId === roomId) {
        setSelectedRoomId(null);
      }
    } catch (error) {
      console.error("Error deleting room:", error);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <ChatSidebar
        chatRooms={chatRooms}
        selectedRoomId={selectedRoomId}
        onRoomSelect={handleRoomSelect}
        onCreateRoom={() => setIsNewRoomDialogOpen(true)}
        onDeleteRoom={handleDeleteRoom}
        setIsLoggedIn={setIsLoggedIn}
        user={user}
      />

      <div className="flex-1 flex flex-col">
        {selectedRoom ? (
          <>
            <div className="bg-white p-4 border-b">
              <h2 className="text-xl font-bold">
                {selectedRoom.chatroom_name}
              </h2>
              {selectedRoom.instructor_name && (
                <p className="text-sm text-gray-500">
                  Instructor: {selectedRoom.instructor_name}
                </p>
              )}
              {selectedRoom.course_code && (
                <p className="text-sm text-gray-500">
                  Course Code: {selectedRoom.course_code}
                </p>
              )}
            </div>

            <ChatMessages messages={selectedRoom.messages} />

            <ChatInput
              inputMessage={inputMessage}
              onInputChange={setInputMessage}
              onSendMessage={handleSendMessage}
              onOpenFileUploadDialog={() => setIsFileUploadDialogOpen(true)}
              selectedFiles={selectedRoom.files}
            />
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <p className="text-gray-500">
              Select a chat room to start messaging
            </p>
          </div>
        )}
      </div>

      <NewRoomDialog
        isOpen={isNewRoomDialogOpen}
        onOpenChange={setIsNewRoomDialogOpen}
        onSubmit={handleNewRoomSubmit}
        newRoomName={newRoomName}
        newRoomInstructor={newRoomInstructor}
        newRoomCourseCode={newRoomCourseCode}
        onNameChange={setNewRoomName}
        onInstructorChange={setNewRoomInstructor}
        onCourseCodeChange={setNewRoomCourseCode}
      />

      <FileUploadDialog
        isOpen={isFileUploadDialogOpen}
        onOpenChange={setIsFileUploadDialogOpen}
        onConfirm={handleFileUpload}
        selectedFiles={selectedRoom?.files || []}
        onFileRemove={handleFileRemove}
      />
    </div>
  );
}
