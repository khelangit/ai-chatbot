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
    <div class="bg-white dark:bg-gray-800 p-4 shadow-lg flex items-center">
      <input v-model="userMessage" @keyup.enter="sendMessage"
        class="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
        placeholder="Type your message..." :disabled="isLoading" />
      <button @click="sendMessage" class="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
        :disabled="isLoading">
        {{ isLoading ? 'Waiting...' : 'Send' }}
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
      processedOutput: "", // Store processed image output
      messages: [],
    };
  },
  methods: {
    toggleImageProcessor() {
      this.showImageProcessor = !this.showImageProcessor;
    },
    handleImageProcessed(imageUrl) {
      this.messages.push({ text: imageUrl, sender: "bot", type: "image" });
      this.processedOutput = result; // Store output
      this.showImageProcessor = false; // Close the overlay
    },
    async sendMessage() {
      if (!this.userMessage.trim() || this.isLoading) return;

      const message = this.userMessage;
      this.userMessage = "";
      this.isLoading = true;

      this.messages.push({ text: message, sender: "user", type: "text" });
      this.isTyping = true;

      try {
        const res = await apiClient.post("/chat", { prompt: message });
        this.isTyping = false;
        this.isLoading = false;
        this.messages.push({ text: res.data.reply, sender: "bot", type: "text" });
      } catch (error) {
        this.isTyping = false;
        this.isLoading = false;
        this.messages.push({ text: "Error: Unable to fetch response.", sender: "bot", type: "text" });
      }
    },
    // BUG FIX: Added missing startNewChat method
    startNewChat() {
      this.showChat = true;
      this.messages = [];
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
          return `<pre class="bg-gray-800 text-white p-3 rounded-lg"><code class="hljs">${highlightedCode}</code></pre>`;
        }
      );
    },
  },
};
</script>

<style scoped>
/* Overlay for Image Processor */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  transition: opacity 0.3s ease-in-out;
}

.overlay-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 80%;
  height: 80%;
  position: relative;
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

.app-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 250px;
  background: #222;
  color: white;
  padding: 10px;
}
</style>
