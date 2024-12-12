import React, { useState, useEffect } from "react";
import { ChatSidebar } from "./ChatSideBar";
import { ChatMessages } from "./ChatMessages";
import { ChatInput } from "./ChatInput";
import { NewRoomDialog } from "./NewRoomDialog";
import FileUploadDialog from "./FileUploadDialog";

export default function ChatInterface({ setIsLoggedIn }) {
  // 채팅방 관련 상태
  const [chatRooms, setChatRooms] = useState([
    { id: 1, name: "e.g., Introduction to AI", messages: [], files: [] },
    { id: 2, name: "e.g., Machine Learning", messages: [], files: [] },
  ]);
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

  // 현재 선택된 채팅방 찾기
  const selectedRoom = chatRooms.find((room) => room.id === selectedRoomId);

  // 메시지 전송 처리
  const handleSendMessage = () => {
    if (inputMessage.trim() && selectedRoomId) {
      const newMessage = {
        id: Date.now(),
        sender: "user",
        content: inputMessage.trim(),
      };
      setChatRooms((prevRooms) =>
        prevRooms.map((room) =>
          room.id === selectedRoomId
            ? { ...room, messages: [...room.messages, newMessage] }
            : room
        )
      );
      setInputMessage("");
    }
  };

  // 새 채팅방 생성 처리
  const handleNewRoomSubmit = () => {
    if (newRoomName) {
      const newRoom = {
        id: Date.now(),
        name: newRoomName,
        instructor: newRoomInstructor || undefined,
        courseCode: newRoomCourseCode || undefined,
        messages: [],
        files: [],
      };
      setChatRooms((prevRooms) => [...prevRooms, newRoom]);
      setIsNewRoomDialogOpen(false);
      setNewRoomName("");
      setNewRoomInstructor("");
      setNewRoomCourseCode("");
      setSelectedRoomId(newRoom.id);
    }
  };

  // 파일 업로드 처리
  const handleFileUpload = (files) => {
    if (selectedRoomId) {
      setChatRooms((prevRooms) =>
        prevRooms.map((room) =>
          room.id === selectedRoomId
            ? { ...room, files: [...room.files, ...files] }
            : room
        )
      );
    }
    setIsFileUploadDialogOpen(false);
  };

  // 파일 제거 처리
  const handleFileRemove = (fileToRemove) => {
    if (selectedRoomId) {
      setChatRooms((prevRooms) =>
        prevRooms.map((room) =>
          room.id === selectedRoomId
            ? {
                ...room,
                files: room.files.filter((file) => file !== fileToRemove),
              }
            : room
        )
      );
    }
  };

  // 채팅방 삭제 처리
  const handleDeleteRoom = (roomId) => {
    setChatRooms((prevRooms) => prevRooms.filter((room) => room.id !== roomId));
    if (selectedRoomId === roomId) {
      setSelectedRoomId(null);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <ChatSidebar
        chatRooms={chatRooms}
        selectedRoomId={selectedRoomId}
        onRoomSelect={setSelectedRoomId}
        onCreateRoom={() => setIsNewRoomDialogOpen(true)}
        onDeleteRoom={handleDeleteRoom}
        setIsLoggedIn={setIsLoggedIn}
      />

      <div className="flex-1 flex flex-col">
        {selectedRoom ? (
          <>
            <div className="bg-white p-4 border-b">
              <h2 className="text-xl font-bold">{selectedRoom.name}</h2>
              {selectedRoom.instructor && (
                <p className="text-sm text-gray-500">
                  Instructor: {selectedRoom.instructor}
                </p>
              )}
              {selectedRoom.courseCode && (
                <p className="text-sm text-gray-500">
                  Course Code: {selectedRoom.courseCode}
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
