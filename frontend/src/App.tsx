import { ChatInterface } from "./components/rag/ChatInterface";
import { ThemeToggle } from "./components/rag/ThemeToggle";

function App() {
  return (
    <div className="min-h-screen bg-background text-foreground transition-colors duration-300 flex flex-col items-center justify-center p-4 md:p-8">
      {/* Top Bar */}
      <div className="absolute top-4 right-4 z-50">
        <ThemeToggle />
      </div>

      <div className="w-full max-w-5xl h-[85vh] flex flex-col">
         {/* Title / Hero */}
         <div className="mb-6 text-center space-y-2">
            <h1 className="text-3xl md:text-4xl font-bold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary/60">
              Enterprise Analyst AI
            </h1>
            <p className="text-muted-foreground text-sm md:text-base max-w-2xl mx-auto">
              Secure, air-gapped retrieval from SEC 10-K Filings. Powered by Hybrid Search & Neural Reranking.
            </p>
         </div>

         <ChatInterface />
      </div>
    </div>
  );
}

export default App;