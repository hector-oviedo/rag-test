import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Send, Sparkles } from "lucide-react";
import { MessageBubble } from "./MessageBubble";
import { Button } from "../ui/button";
import { cn } from "../../lib/utils";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: any[];
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hello. I am your Sovereign Financial Analyst. I have access to the secure 10-K filings. How can I assist you today?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setIsLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/chat", {
        message: userMsg,
      });

      const data = response.data;
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
        },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "I encountered an error connecting to the secure backend. Please ensure the local API is running.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full max-w-4xl mx-auto bg-card shadow-2xl rounded-xl overflow-hidden border border-border">
      {/* Header */}
      <div className="p-4 border-b border-border bg-muted/20 flex items-center gap-2 backdrop-blur-md">
        <Sparkles className="w-5 h-5 text-primary" />
        <h2 className="font-semibold text-sm tracking-tight">Sovereign RAG v1.0</h2>
        <div className="ml-auto flex items-center gap-2 text-xs text-muted-foreground">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
          System Online
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-secondary">
        {messages.map((msg, idx) => (
          <MessageBubble
            key={idx}
            role={msg.role}
            content={msg.content}
            sources={msg.sources}
          />
        ))}
        {isLoading && (
          <MessageBubble role="assistant" content="" isTyping={true} />
        )}
        <div ref={scrollRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-background border-t border-border">
        <form onSubmit={handleSubmit} className="relative flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about risk factors, financials, or strategy..."
            className="flex-1 bg-secondary/50 text-foreground placeholder:text-muted-foreground border-none rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
            disabled={isLoading}
          />
          <Button
            type="submit"
            size="icon"
            disabled={isLoading || !input.trim()}
            className={cn(
              "absolute right-2 transition-all duration-300",
              input.trim() ? "scale-100 opacity-100" : "scale-90 opacity-0"
            )}
          >
            <Send className="w-4 h-4" />
          </Button>
        </form>
        <div className="text-center mt-2">
           <span className="text-[10px] text-muted-foreground uppercase tracking-widest opacity-50">
             Protected Mode • Local Inference Only
           </span>
        </div>
      </div>
    </div>
  );
}
