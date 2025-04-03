<template>
  <div class="flex flex-col h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Header -->
    <header class="bg-blue-600 text-white text-center py-4 shadow-lg flex justify-between px-4">
      <h1 class="text-2xl font-bold">AI Chatbot</h1>
      <!-- Image to Code Button -->
      <button @click="toggleImageProcessor"
        class="px-4 py-2 bg-white text-blue-600 rounded-lg shadow-md hover:bg-gray-200">
        Image to Code
      </button>
    </header>

    <!-- Image Processor Overlay -->
    <div v-if="showImageProcessor" class="overlay">
      <div class="overlay-content">
        <button @click="toggleImageProcessor" class="close-btn">✖ Close</button>
        <image-processor @imageProcessed="handleImageProcessed" />
      </div>
    </div>

    <!-- Show Processed Image Output in Chat -->
    <div v-if="processedOutput" class="bg-gray-200 p-4 rounded-md m-4 shadow-lg">
      <h3 class="text-lg font-bold">🖼 Image Processing Result:</h3>
      <pre class="bg-white p-3 rounded-md">{{ processedOutput }}</pre>
    </div>

    <!-- Chat Component -->
    <div v-if="!showChat" class="flex justify-center items-center h-full">
      <button @click="startNewChat"
        class="px-6 py-3 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition">
        ➕ Start New Chat
      </button>
    </div>

    <div v-if="showChat" class="app-container">
      <!-- Sidebar -->
      <aside class="sidebar">
        <button @click="startNewChat"
          class="mt-4 px-6 py-3 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition">
          ➕ Start New Chat
        </button>
        <hr>
        <h3>Chat History</h3>
        <ul v-if="chatHistory.length">
          <li v-for="(chat, index) in chatHistory" :key="index">
            <span @click="loadChat(chat)" class="cursor-pointer hover:text-blue-400">
              {{ chat.title }}
            </span>
            <button @click="deleteChat(index)" class="ml-2 text-red-500 hover:text-red-700">🗑</button>
          </li>
        </ul>
        <p v-else class="text-gray-400 text-sm text-center mt-2">No history yet.</p>
      </aside>

      <!-- Chat Box -->
      <div ref="chatContainer" class="flex-1 overflow-y-scroll p-4 space-y-4 min-h-0">
        <div v-for="(msg, index) in messages" :key="index" class="flex items-start relative"
          :class="msg.sender === 'user' ? 'justify-end' : 'justify-start'">
          <div class="rounded-xl px-5 py-3 shadow-md w-fit max-w-md whitespace-pre-wrap font-mono transition-all duration-300 text-lg relative"
            :class="msg.sender === 'user' ? 'bg-blue-500 text-white rounded-br-none' : 'bg-gray-300 dark:bg-gray-700 text-black dark:text-white rounded-bl-none'">
            <p v-if="msg.type === 'text'" v-html="formatMessage(msg.text)"></p>
            <img v-if="msg.type === 'image'" :src="msg.text" alt="Processed Image" class="rounded-lg shadow-md max-w-xs">
          </div>
        </div>

        <!-- Loading Animation -->
        <div v-if="isTyping" class="flex justify-start items-center space-x-2">
          <div
            class="bg-gray-300 dark:bg-gray-700 text-black dark:text-white px-5 py-3 rounded-lg shadow-md w-fit max-w-md">
            <span class="typing-dots"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Box -->
    <div class="bg-white dark:bg-gray-800 p-4 shadow-lg flex items-center sticky bottom-0">
      <input 
        v-model="userMessage" 
        @keyup.enter="sendMessage"
        class="flex-1 p-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white transition-all duration-200"
        placeholder="Type your message..." 
        :disabled="isLoading"/>
      <button 
        @click="sendMessage" 
        class="ml-3 px-5 py-2.5 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200 shadow-md"
        :disabled="isLoading"
        :class="{ 'opacity-50 cursor-not-allowed': isLoading }"
      >
        {{ isLoading ? 'Sending...' : 'Send' }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { marked } from "marked";
import hljs from "highlight.js";
import "highlight.js/styles/github.css";
import ImageProcessor from "./ImageProcessor.vue";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 120000,
  headers: { "Content-Type": "application/json" },
});

export default {
  components: {
    ImageProcessor,
  },

  data() {
    return {
      chatHistory: [],
      userMessage: "",
      isTyping: false,
      isLoading: false,
      showChat: false,
      showImageProcessor: false,
      processedOutput: null, // Changed to null for better state tracking
      messages: [],
      currentChatId: null, // Track active chat
    };
  },
  methods: {
    toggleImageProcessor() {
      this.showImageProcessor = !this.showImageProcessor;
      if (!this.showImageProcessor) {
        this.processedOutput = null;
      }
    },
    handleImageProcessed(result) { // Fixed parameter name
      if (result && result.output_image) {
        this.messages.push({
          text: result.output_image,
          sender: "bot",
          type: "image"
        });
        if (result.extracted_text) {
          this.messages.push({
            text: `Extracted text: ${result.extracted_text}`,
            sender: "bot",
            type: "text"
          });
        }
      }
      this.showImageProcessor = false;
    },
    async sendMessage() {
      if (!this.userMessage.trim() || this.isLoading) return;

      const message = this.userMessage;
      this.userMessage = "";
      this.isLoading = true;

      this.messages.push({ text: message, sender: "user", type: "text" });
      this.isTyping = true;

      try {
        const res = await apiClient.post("/chat", { 
          prompt: message,
          chatId: this.currentChatId 
        });
        
        if (res.data.chatId && !this.currentChatId) {
          this.currentChatId = res.data.chatId;
        }

        this.messages.push({
          text: res.data.reply,
          sender: "bot",
          type: "text"
        });
      } catch (error) {
        console.error("Chat error:", error);
        this.messages.push({
          text: "Sorry, I encountered an error. Please try again.",
          sender: "bot",
          type: "text"
        });
      } finally {
        this.isTyping = false;
        this.isLoading = false;
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    startNewChat() {
      this.showChat = true;
      this.messages = [];
      this.currentChatId = null;
      this.processedOutput = null;
    },
    scrollToBottom() {
      const container = this.$refs.chatContainer;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
    // Placeholder methods for loadChat and deleteChat
    loadChat(chat) {
      // Implementation to load a specific chat from history
      this.messages = chat.messages;
    },
    deleteChat(index) {
      this.chatHistory.splice(index, 1);
    },
    formatMessage(text) {
      let markdownText = marked.parse(text);
      return markdownText.replace(
        /<pre><code class="([^"]*)">([\s\S]*?)<\/code><\/pre>/g,
        (match, lang, code) => {
          const highlightedCode = hljs.highlightAuto(code).value;
          return `<pre class="bg-gray-800 text-white p-2 rounded-lg"><code class="hljs">${highlightedCode}</code></pre>`;
        }
      );
    },
  },
  mounted() {
    this.loadChatHistory();
  }
};
</script>

<style scoped>
/* Improved overlay styling */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.overlay-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: auto;
  position: relative;
}

/* Improved message bubbles */
.message-bubble {
  max-width: 80%;
  word-wrap: break-word;
  margin-bottom: 0.5rem;
}

.user-message {
  align-self: flex-end;
  background: #3b82f6;
  color: white;
  border-radius: 18px 18px 0 18px;
}

.bot-message {
  align-self: flex-start;
  background: #f3f4f6;
  color: #111827;
  border-radius: 18px 18px 18px 0;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: red;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 16px;
}

.typing-dots::after {
  content: " .";
  animation: dots 1.5s steps(3, end) infinite;
}

@keyframes dots {
  0% {
    content: " .";
  }

  33% {
    content: " ..";
  }

  66% {
    content: " ...";
  }

  100% {
    content: " .";
  }
}

/* Main container styling */
.app-container {
  display: flex;
  height: calc(100vh - 120px);
  width: 100%;
  max-width: 100%;
}

/* Chat container styling */
.chat-container {
  width: 100%;
  max-width: 100%;
  height: 100%;
  margin: 0;
  padding: 1rem;
  overflow-y: auto;
}

/* Input box container styling */
.bg-white.dark\:bg-gray-800 {
  width: 100%;
  max-width: 100%;
  margin: 0;
  border-radius: 0;
  position: fixed;
  bottom: 0;
  padding: 1rem;
}

/* Message container styling */
.flex.items-start.relative {
  width: 100%;
  max-width: 100%;
  margin: 0 auto 1rem;
  padding: 0 1rem;
}

/* Sidebar styling */
.sidebar {
  width: 280px;
  min-width: 280px;
  max-width: 280px;
}

/* Message bubbles */
.message-bubble {
  max-width: 90%;
}

/* Overlay content */
.overlay-content {
  width: 95%;
  max-width: 800px;
}

/* Hide scrollbar for chat messages */
.chat-container::-webkit-scrollbar {
  display: none;
  width: 0;
  height: 0;
}

.sidebar {
  width: 250px;
  background: #222;
  color: white;
  padding: 10px;
}
</style>
