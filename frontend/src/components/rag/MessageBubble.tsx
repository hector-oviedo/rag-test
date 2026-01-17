import React from "react";
import { cn } from "../../lib/utils";
import { Bot, User } from "lucide-react";
import { SourceCard } from "./SourceCard";

interface MessageProps {
  role: "user" | "assistant";
  content: string;
  sources?: any[]; // Using any for simplicity here, matches SourceNode
  isTyping?: boolean;
}

export function MessageBubble({ role, content, sources, isTyping }: MessageProps) {
  return (
    <div
      className={cn(
        "flex w-full gap-4 p-6 transition-colors",
        role === "assistant" ? "bg-muted/30" : "bg-background"
      )}
    >
      <div className="flex-shrink-0 mt-1">
        <div
          className={cn(
            "h-8 w-8 rounded-full flex items-center justify-center border",
            role === "assistant"
              ? "bg-primary text-primary-foreground border-primary"
              : "bg-secondary text-secondary-foreground border-border"
          )}
        >
          {role === "assistant" ? <Bot className="w-5 h-5" /> : <User className="w-5 h-5" />}
        </div>
      </div>

      <div className="flex-1 space-y-4">
        <div className="prose prose-sm dark:prose-invert max-w-none leading-7">
          {isTyping ? (
            <span className="animate-pulse">Thinking...</span>
          ) : (
            <div className="whitespace-pre-wrap">{content}</div>
          )}
        </div>

        {sources && sources.length > 0 && (
          <div className="mt-6 pt-4 border-t border-border">
            <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
              Verified Sources
            </h4>
            <div className="grid grid-cols-1 gap-2">
              {sources.map((source, idx) => (
                <SourceCard key={idx} source={source} index={idx} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
