import { ScrollArea } from "@/components/ui/scroll-area";
import { useRef, useEffect, useState } from "react";
import { TypeAnimation } from "react-type-animation";

export function ChatMessages({ messages }) {
  const messagesEndRef = useRef(null);
  const [animatingMessageId, setAnimatingMessageId] = useState(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      if (lastMessage.sender_type === "bot") {
        setAnimatingMessageId(lastMessage.message_id);
      }
    }
    scrollToBottom();
  }, [messages]);

  return (
    <ScrollArea className="flex-1 p-4 h-[calc(100vh-250px)]">
      {messages.map((message) => (
        <div
          key={message.message_id}
          className={`mb-3 ${
            message.sender_type === "user" ? "text-right" : "text-left"
          }`}
        >
          <div
            className={`inline-block p-1.5 px-3 rounded-lg ${
              message.sender_type === "user"
                ? "bg-skkuGreen text-white"
                : "bg-gray-200"
            }`}
          >
            {message.sender_type === "bot" &&
            message.message_id === animatingMessageId ? (
              <TypeAnimation
                sequence={[message.content]}
                wrapper="span"
                speed={80}
                cursor={false}
                repeat={0}
                onComplete={() => setAnimatingMessageId(null)}
              />
            ) : (
              message.content
            )}
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </ScrollArea>
  );
}
