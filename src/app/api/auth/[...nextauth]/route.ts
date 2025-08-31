import NextAuth, { NextAuthOptions } from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials"

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        // 👇 Dummy authentication (replace with DB later)
        if (
          credentials?.email === "admin@gmail.com" &&
          credentials?.password === "admin"
        ) {
          return {
            id: "1",
            name: "Admin User",
            email: "admin@example.com",
          }
        }
        return null
      },
    }),
  ],
  pages: {
    signIn: "/login", // custom login page
  },
  secret: process.env.NEXTAUTH_SECRET,
}

const handler = NextAuth(authOptions)
export { handler as GET, handler as POST }