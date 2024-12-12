import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { PlusCircle, LogOut, Trash2 } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

export function ChatSidebar({
  chatRooms,
  selectedRoomId,
  onRoomSelect,
  onCreateRoom,
  onDeleteRoom,
  setIsLoggedIn = () => {},
  user,
}) {
  const [showLogout, setShowLogout] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [contextMenu, setContextMenu] = useState(null);
  const navigate = useNavigate();

  const contextMenuRef = useRef(null);

  const handleLogout = async () => {
    try {
      setIsLoading(true);
      Cookies.remove("access_token", { path: "/" });
      Cookies.remove("refresh_token", { path: "/" });
      setIsLoggedIn(false);
      alert("Logged out.");
      navigate("/login");
    } catch (error) {
      console.error("로그아웃 중 오류가 발생했습니다:", error);
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
        <div
          onClick={() => window.location.reload()}
          className="text-2xl font-bold mb-4 mt-1 text-center cursor-pointer"
        >
          Studymates Hub
        </div>
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
            key={room.chatroom_id}
            onClick={() => onRoomSelect(room.chatroom_id)}
            onContextMenu={(e) => handleContextMenu(e, room.chatroom_id)}
            className={`w-full text-left p-4 rounded-none transition-transform duration-300 ease-in-out transform hover:-translate-y-1 border-none outline-none focus:outline-none ${
              selectedRoomId === room.chatroom_id
                ? "bg-skkuGreen text-white"
                : ""
            }`}
          >
            {room.chatroom_name}
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
            <span className="font-medium">
              {user ? `${user.first_name} ${user.last_name}` : "Loading..."}
            </span>
            <span className="text-sm text-gray-500">
              {user ? user.email : "Loading..."}
            </span>
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
