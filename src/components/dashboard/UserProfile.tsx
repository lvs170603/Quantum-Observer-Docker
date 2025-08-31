"use client"

import { useState } from "react"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

interface UserProfileProps {
  name: string
  email: string
  avatarUrl?: string
  role?: string
}

export default function UserProfile({ name, email, avatarUrl, role }: UserProfileProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [userName, setUserName] = useState(name)
  const [userEmail, setUserEmail] = useState(email)

  const handleSave = () => {
    setIsEditing(false)
    // 🔥 Save logic here (API call / DB update)
    console.log("Updated:", { userName, userEmail })
  }

  return (
    <Card className="w-full max-w-md mx-auto shadow-lg rounded-2xl">
      <CardHeader className="flex items-center gap-4">
        <Avatar className="w-16 h-16">
          <AvatarImage src={avatarUrl} alt={name} />
          <AvatarFallback>{name.charAt(0)}</AvatarFallback>
        </Avatar>
        <div>
          <CardTitle className="text-xl font-semibold">{userName}</CardTitle>
          <p className="text-sm text-muted-foreground">{role ?? "User"}</p>
        </div>
      </CardHeader>

      <CardContent>
        {isEditing ? (
          <div className="space-y-4">
            <div>
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={userEmail}
                onChange={(e) => setUserEmail(e.target.value)}
              />
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            <p><span className="font-medium">Email:</span> {userEmail}</p>
            <p><span className="font-medium">Role:</span> {role ?? "User"}</p>
          </div>
        )}
      </CardContent>

      <CardFooter className="flex justify-end gap-2">
        {isEditing ? (
          <>
            <Button variant="outline" onClick={() => setIsEditing(false)}>Cancel</Button>
            <Button onClick={handleSave}>Save</Button>
          </>
        ) : (
          <Button onClick={() => setIsEditing(true)}>Edit Profile</Button>
        )}
      </CardFooter>
    </Card>
  )
}
