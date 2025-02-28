
<template>
    <div class="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4">
      <h2 class="text-xl font-semibold text-gray-800">Image Processor</h2>
  
      <input type="file" @change="handleFileUpload" accept="image/*" class="border p-2 rounded w-full" />
  
      <button @click="processImage" :disabled="!selectedFile" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400">
        Upload & Process
      </button>
  
      <div v-if="loading" class="text-blue-500">Processing...</div>
  
      <div v-if="result" class="mt-4 p-3 bg-gray-100 rounded">
        <h3 class="font-semibold">Response:</h3>
        <p class="text-sm">{{ result }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        selectedFile: null,
        loading: false,
        result: null
      };
    },
    methods: {
      handleFileUpload(event) {
        this.selectedFile = event.target.files[0];
      },
      async processImage() {
        if (!this.selectedFile) {
          alert("Please select an image first.");
          return;
        }
  
        this.loading = true;
        const formData = new FormData();
        formData.append("image", this.selectedFile);
  
        try {
          const response = await axios.post("http://127.0.0.1:8000/api/imageprocess", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });
          this.result = response.data;
        } catch (error) {
          console.error("Error processing image:", error);
          alert("Error processing image.");
        } finally {
          this.loading = false;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  button:disabled {
    cursor: not-allowed;
  }
  </style>
  