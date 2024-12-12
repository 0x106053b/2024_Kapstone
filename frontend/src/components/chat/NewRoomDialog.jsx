import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function NewRoomDialog({
  isOpen,
  onOpenChange,
  onSubmit,
  newRoomName,
  newRoomInstructor,
  newRoomCourseCode,
  onNameChange,
  onInstructorChange,
  onCourseCodeChange,
}) {
  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="bg-white text-black">
        <DialogHeader>
          <DialogTitle>Create New Chat Room</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              Course Name <span className="text-red-500">*</span>
            </Label>
            <Input
              id="name"
              value={newRoomName}
              onChange={(e) => onNameChange(e.target.value)}
              className="col-span-3"
              placeholder="Enter new Course Name"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="instructor" className="text-right">
              Instructor
            </Label>
            <Input
              id="instructor"
              value={newRoomInstructor}
              onChange={(e) => onInstructorChange(e.target.value)}
              className="col-span-3"
              placeholder="optional"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="courseCode" className="text-right">
              Course Code
            </Label>
            <Input
              id="courseCode"
              value={newRoomCourseCode}
              onChange={(e) => onCourseCodeChange(e.target.value)}
              className="col-span-3"
              placeholder="optional"
            />
          </div>
        </div>
        <DialogFooter>
          <Button
            onClick={onSubmit}
            className={`w-full ${
              !newRoomName
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-black text-white"
            }`}
            disabled={!newRoomName}
          >
            Create Room
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
