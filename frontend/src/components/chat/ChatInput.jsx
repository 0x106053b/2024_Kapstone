import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Send, Paperclip } from "lucide-react";
import { useRef, useEffect } from "react";

export function ChatInput({
  inputMessage,
  onInputChange,
  onSendMessage,
  onOpenFileUploadDialog,
}) {
  const textareaRef = useRef(null);

  const adjustHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      const lineHeight = 24;
      const minHeight = 70;
      const maxHeight = lineHeight * 10;

      textarea.style.height = `${minHeight}px`;
      const scrollHeight = textarea.scrollHeight;

      const newHeight = Math.min(Math.max(scrollHeight, minHeight), maxHeight);
      textarea.style.height = `${newHeight}px`;
    }
  };

  useEffect(() => {
    adjustHeight();
  }, [inputMessage]);

  return (
    <div className="p-4 bg-white border-t">
      <div className="flex flex-col space-y-2">
        <Textarea
          value={inputMessage}
          onChange={(e) => onInputChange(e.target.value)}
          ref={textareaRef}
          placeholder="Type your message..."
          className="flex-grow min-h-[70px] max-h-[150px] resize-none"
          onKeyPress={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              onSendMessage();
            }
          }}
        />
        <div className="flex justify-between">
          <div>
            <Button
              onClick={onOpenFileUploadDialog}
              variant="outline"
              className="hover:bg-gray-200 transition-colors duration-200 ease-in-out border border-gray-200"
            >
              <Paperclip className="h-4 w-4 mr-2" />
              Attach Files
            </Button>
          </div>
          <Button
            onClick={onSendMessage}
            className="hover:bg-gray-200 transition-colors duration-200 ease-in-out border border-gray-200"
          >
            <Send className="h-4 w-4 mr-2" /> Send
          </Button>
        </div>
      </div>
    </div>
  );
}
