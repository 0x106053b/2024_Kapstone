import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { PlusCircle, LogOut, Trash2 } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export function ChatSidebar({
  chatRooms,
  selectedRoomId,
  onRoomSelect,
  onCreateRoom,
  onDeleteRoom,
  setIsLoggedIn = () => {},
}) {
  const [showLogout, setShowLogout] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [contextMenu, setContextMenu] = useState(null);
  const navigate = useNavigate();

  const contextMenuRef = useRef(null);

  //임시 유저 데이터
  const user = {
    name: "Sungkyun Kim",
    id: "Sungkyun.kim@example.com",
  };

  const handleLogout = async () => {
    try {
      setIsLoading(true);
      console.log("Logging out...", setIsLoggedIn);

      if (typeof setIsLoggedIn === "function") {
        setIsLoggedIn(false);
        await new Promise((resolve) => setTimeout(resolve, 1000));
        navigate("/login");
      } else {
        console.error("setIsLoggedIn is not a function:", setIsLoggedIn);
      }
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleContextMenu = (e, roomId) => {
    e.preventDefault();
    setContextMenu({
      x: e.clientX,
      y: e.clientY,
      roomId: roomId,
    });
  };

  const handleDeleteRoom = () => {
    if (contextMenu) {
      onDeleteRoom(contextMenu.roomId);
      setContextMenu(null);
    }
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        contextMenuRef.current &&
        !contextMenuRef.current.contains(event.target)
      ) {
        setContextMenu(null);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  // 채팅방 목록을 역순으로 정렬
  const sortedChatRooms = [...chatRooms].reverse();

  return (
    <div className="w-64 bg-white border-r flex flex-col h-full">
      <div className="p-4">
        <h2 className="text-2xl font-bold mb-4 mt-1 text-center">
          Studymates Hub
        </h2>
        <Button
          onClick={onCreateRoom}
          className="w-full mb-4 bg-black text-white hover:bg-gray-500"
        >
          <PlusCircle className="mr-2 h-4 w-4" /> New Chat Room
        </Button>
      </div>

      <ScrollArea className="flex-1">
        {sortedChatRooms.map((room) => (
          <button
            key={room.id}
            onClick={() => onRoomSelect(room.id)}
            onContextMenu={(e) => handleContextMenu(e, room.id)}
            className={`w-full text-left p-4 rounded-none transition-transform duration-300 ease-in-out transform hover:-translate-y-1 border-none outline-none focus:outline-none ${
              selectedRoomId === room.id ? "bg-skkuGreen text-white" : ""
            }`}
          >
            {room.name}
          </button>
        ))}
      </ScrollArea>

      {contextMenu && (
        <div
          ref={contextMenuRef}
          style={{
            position: "fixed",
            top: contextMenu.y,
            left: contextMenu.x,
            zIndex: 1000,
          }}
          className="bg-white border rounded shadow-lg"
        >
          <button
            onClick={handleDeleteRoom}
            className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center"
          >
            <Trash2 className="mr-2 h-4 w-4 text-red-500" />
            Delete Room
          </button>
        </div>
      )}

      <div className="border-t p-4">
        <div className="relative">
          <button
            onClick={() => setShowLogout(!showLogout)}
            className="w-full flex flex-col items-start hover:bg-gray-100 p-2 rounded-lg transition-colors duration-200"
          >
            <span className="font-medium">{user.name}</span>
            <span className="text-sm text-gray-500">{user.id}</span>
          </button>

          {showLogout && (
            <div className="absolute bottom-full left-0 mb-2 w-full bg-white shadow-lg rounded-lg border overflow-hidden">
              <button
                onClick={handleLogout}
                disabled={isLoading}
                className="w-full flex items-center px-4 py-2 text-red-600 hover:bg-gray-100 transition-colors duration-200"
              >
                <LogOut className="h-4 w-4 mr-2" />
                {isLoading ? "Logging out..." : "Logout"}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
