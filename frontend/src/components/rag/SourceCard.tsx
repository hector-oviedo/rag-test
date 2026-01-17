import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, FileText, Gauge } from "lucide-react";
import { cn } from "../../lib/utils";

interface SourceNode {
  file_name: string;
  page_label: string;
  score: float;
  content: string;
}

interface SourceCardProps {
  source: SourceNode;
  index: number;
}

export function SourceCard({ source, index }: SourceCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  // Calculate reliability color based on score
  const scoreColor =
    source.score > 0.85
      ? "text-green-500"
      : source.score > 0.75
      ? "text-yellow-500"
      : "text-red-500";

  return (
    <div className="border border-border rounded-lg overflow-hidden bg-card/50 backdrop-blur-sm mb-2 transition-all hover:border-primary/50">
      <div
        className="flex items-center justify-between p-3 cursor-pointer hover:bg-accent/50"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-secondary flex items-center justify-center text-xs font-mono">
            {index + 1}
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-medium flex items-center gap-1">
              <FileText className="w-3 h-3 text-muted-foreground" />
              {source.file_name}
            </span>
            <span className="text-xs text-muted-foreground flex items-center gap-1">
              <Gauge className="w-3 h-3" />
              Relevance: <span className={scoreColor}>{(source.score * 100).toFixed(1)}%</span>
            </span>
          </div>
        </div>
        <ChevronDown
          className={cn(
            "w-4 h-4 text-muted-foreground transition-transform duration-200",
            isExpanded ? "transform rotate-180" : ""
          )}
        />
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="p-3 pt-0 text-sm text-muted-foreground border-t border-border/50 bg-secondary/20">
              <div className="font-mono text-xs mb-1 text-primary opacity-70">
                RAW CONTEXT EXTRACT:
              </div>
              <p className="whitespace-pre-wrap leading-relaxed">
                {source.content}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
