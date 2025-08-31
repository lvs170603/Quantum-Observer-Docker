"use client"

import * as React from "react"
import { User } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog"

import UserProfile from "@/components/dashboard/UserProfile"

export function UserButton() {
  const [open, setOpen] = React.useState(false)

  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" size="icon">
            <User className="h-[1.2rem] w-[1.2rem]" />
            <span className="sr-only">Open user menu</span>
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent align="end">
          <DropdownMenuItem onClick={() => setOpen(true)}>
            Profile
          </DropdownMenuItem>
          {/* <DropdownMenuItem onClick={() => alert("Settings clicked!")}>
            Settings
          </DropdownMenuItem> */}
          <DropdownMenuItem
              onClick={() => {
                localStorage.removeItem("isLoggedIn")   // ✅ Clear login flag
                window.location.href = "/login"         // ✅ Redirect to login page
              }}
            >
              Logout
          </DropdownMenuItem>

        </DropdownMenuContent>
      </DropdownMenu>

      {/* Dialog for Profile */}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>User Profile</DialogTitle>
            <DialogDescription>
              Manage your account details.
            </DialogDescription>
          </DialogHeader>

          {/* User Profile Component */}
          <UserProfile
            name="L. Venkata Sai"
            email="Lvs1706@gmail.com"
            // avatarUrl="/userlogo.png"
            role="Developer"
          />
        </DialogContent>
      </Dialog>
    </>
  )
}
