<template>
  <div class="flex flex-col h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Header -->
    <header class="bg-blue-600 text-white text-center py-4 shadow-lg">
      <h1 class="text-2xl font-bold">AI Chatbot</h1>
    </header>
    <div v-if="!showChat" class="flex justify-center items-center h-full">
      <button @click="startNewChat"
        class="px-6 py-3 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition">
        ➕ Start New Chat
      </button>
    </div>


    <div v-if="showChat" class="app-container">
      <!-- Sidebar -->
      <aside class="sidebar">
        <!-- Button to start new chat -->
        <button @click="startNewChat"
          class="mt-4 px-6 py-3 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition">
          ➕ Start New Chat
        </button>
        <hr>
        <h3>Chat History</h3>

        <!-- Display Chat History -->
        <ul v-if="chatHistory.length">
          <li v-for="(chat, index) in chatHistory" :key="index">
            <span @click="loadChat(chat)" class="cursor-pointer hover:text-blue-400">
              {{ chat.title }}
            </span>
            <button @click="deleteChat(index)" class="ml-2 text-red-500 hover:text-red-700">🗑</button>
          </li>
        </ul>

        <!-- Message when no history exists -->
        <p v-else class="text-gray-400 text-sm text-center mt-2">No history yet.</p>

      </aside>


      <!-- Chat Box -->
      <div ref="chatContainer" class="flex-1 overflow-y-scroll p-4 space-y-4 min-h-0">
        <div v-for="(msg, index) in messages" :key="index" class="flex items-start relative"
          :class="msg.sender === 'user' ? 'justify-end' : 'justify-start'">
          <div
            class="rounded-xl px-5 py-3 shadow-md         w-fit max-w-md whitespace-pre-wrap font-mono transition-all duration-300 text-lg relative"
            :class="msg.sender === 'user' ? 'bg-blue-500 text-white rounded-br-none' : 'bg-gray-300 dark:bg-gray-700 text-black dark:text-white rounded-bl-none'">
            <p v-html="formatMessage(msg.text)"></p>
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
import "highlight.js/styles/github.css"; // Code syntax highlighting theme

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 120000,
  headers: { "Content-Type": "application/json" },
});

export default {
  data() {
    return {
      chatHistory: [],
      userMessage: "",
      messages: [],
      isTyping: false,
      isLoading: false, // Disable input when true
      showChat: false, // ✅ Chat UI hide/show control
    };
  },
  mounted() {
    this.loadHistory(); // Load chat history from localStorage when the app starts
  },
  methods: {
    startNewChat() {
      this.showChat = true;  // Show the chat UI
      this.messages = [];    // Clear previous messages
      this.userMessage = ""; // Clear user input field

      // Save new chat history
      this.saveChatHistory();
    },

    // Load previous chat history from localStorage
    loadHistory() {
      const history = JSON.parse(localStorage.getItem("chatHistory")) || [];
      this.chatHistory = history;
    },

    // Save current chat to chat history
    saveChatHistory() {
      if (this.messages.length === 0) return;

      const newChat = {
        title: this.messages[0]?.text.slice(0, 20) || "New Chat", // Use first message as title
        messages: [...this.messages] // Save the entire chat
      };

      // Add new chat to the beginning of history
      this.chatHistory.unshift(newChat);

      // Save updated history to localStorage
      localStorage.setItem("chatHistory", JSON.stringify(this.chatHistory));
    },

    // Load specific chat history
    loadChat(chat) {
      this.messages = chat.messages;
    },

    // Delete chat from history
    deleteChat(index) {
      this.chatHistory.splice(index, 1);
      localStorage.setItem("chatHistory", JSON.stringify(this.chatHistory));
    },
    async sendMessage() {
      if (!this.userMessage.trim() || this.isLoading) return;

      const message = this.userMessage;
      this.userMessage = "";
      this.isLoading = true; // Disable input & button

      this.messages.push({ text: message, sender: "user" });
      this.isTyping = true;

      try {
        const res = await apiClient.post("/chat", { prompt: message });
        this.isTyping = false;
        this.isLoading = false;
        this.messages.push({ text: res.data.reply, sender: "bot" });
      } catch (error) {
        this.isTyping = false;
        this.isLoading = false;
        this.messages.push({ text: "Error: Unable to fetch response.", sender: "bot" });
      }

      this.saveChatHistory();
      this.scrollToBottom();
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.chatContainer;
        container.scrollTop = container.scrollHeight;
      });
    },
    formatMessage(text) {
      if (!text) return "";
      let markdownText = marked.parse(text);
      return markdownText.replace(
        /<pre><code class="([^"]*)">([\s\S]*?)<\/code><\/pre>/g,
        (match, lang, code) => {
          const highlightedCode = hljs.highlightAuto(code).value;
          return `<pre class="bg-gray-800 text-white p-3 rounded-lg"><code class="hljs">${highlightedCode}</code></pre>`;
        }
      );
    }
  },
};
</script>

<style scoped>
/* Typing Animation */
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

/* Disabled Button */
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Smooth Chat Bubble Transition */
div[role="message"] {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.app-container {
  display: flex;
  height: 100vh;
  overflow-y: auto;
}

.sidebar {
  width: 250px;
  background: #222;
  color: white;
  padding: 10px;
  overflow-y: auto;
}

.sidebar h3 {
  text-align: center;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 8px;
  cursor: pointer;
  border-bottom: 1px solid gray;
  display: flex;
  justify-content: space-between;
}

.sidebar li:hover {
  background: #333;
}

.sidebar button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}
</style>
