<script setup lang="ts">
import { cn } from "@/lib/utils";

interface ChatMessage {
  id: string;
  content: string;
  timestamp: Date;
  sender: "user" | "bot";
  avatar?: string;
}

defineProps<{
  /**
   * The message object to display
   */
  message: ChatMessage;
}>();

const formatTime = (date: Date) => {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};
</script>

<template>
  <div
    :class="
      cn(
        'flex gap-3 max-w-[85%]',
        message.sender === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto'
      )
    "
  >
    <!-- Avatar -->
    <div
      :class="
        cn(
          'w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium flex-shrink-0',
          message.sender === 'user'
            ? 'bg-primary text-primary-foreground'
            : 'bg-muted text-muted-foreground'
        )
      "
    >
      {{ message.sender === "user" ? "You" : "Bot" }}
    </div>

    <!-- Message content -->
    <div
      :class="
        cn(
          'flex flex-col gap-1',
          message.sender === 'user' ? 'items-end' : 'items-start'
        )
      "
    >
      <!-- Message bubble -->
      <div
        :class="
          cn(
            'px-3 py-2 rounded-lg text-sm max-w-xs break-words',
            message.sender === 'user'
              ? 'bg-primary text-primary-foreground rounded-br-sm'
              : 'bg-muted text-foreground rounded-bl-sm'
          )
        "
      >
        {{ message.content }}
      </div>

      <!-- Timestamp -->
      <div
        :class="
          cn(
            'text-xs text-muted-foreground',
            message.sender === 'user' ? 'text-right' : 'text-left'
          )
        "
      >
        {{ formatTime(message.timestamp) }}
      </div>
    </div>
  </div>
</template>
