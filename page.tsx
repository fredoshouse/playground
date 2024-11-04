import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Playground, Shapes, Palette, Sparkles } from "lucide-react"

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-blue-100 to-green-100">
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex items-center justify-between">
          <div className="flex items-center">
            <Playground className="h-8 w-8 text-blue-500 mr-2" />
            <h1 className="text-3xl font-bold text-gray-900">Fredo's Playground</h1>
          </div>
          <nav>
            <Button variant="ghost">About</Button>
            <Button variant="ghost">Activities</Button>
            <Button variant="ghost">Contact</Button>
          </nav>
        </div>
      </header>

      <main className="flex-grow container mx-auto px-4 py-8">
        <h2 className="text-4xl font-bold text-center mb-8">Welcome to the Fun Zone!</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Shapes className="h-6 w-6 mr-2 text-purple-500" />
                Exciting Games
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>Discover a world of fun with our collection of exciting games for all ages!</CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Palette className="h-6 w-6 mr-2 text-orange-500" />
                Creative Corner
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>Let your imagination run wild in our creative corner filled with art supplies and inspiration!</CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Sparkles className="h-6 w-6 mr-2 text-yellow-500" />
                Magic Shows
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>Be amazed by our spectacular magic shows that will leave you wondering, "How did they do that?"</CardDescription>
            </CardContent>
          </Card>
        </div>

        <div className="mt-12 text-center">
          <Button size="lg" className="bg-blue-500 hover:bg-blue-600 text-white">
            Start Playing Now!
          </Button>
        </div>
      </main>

      <footer className="bg-gray-800 text-white py-6">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2023 Fredo's Playground. All rights reserved.</p>
          <p className="mt-2">123 Fun Street, Playville, PL 12345</p>
          <p className="mt-2">Phone: (555) 123-4567 | Email: fun@fredosplayground.com</p>
        </div>
      </footer>
    </div>
  )
}