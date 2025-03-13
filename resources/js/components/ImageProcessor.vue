<template>
  <div class="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4">
    <h2 class="text-xl font-semibold text-gray-800">Image Processor</h2>

    <input type="file" @change="handleFileUpload" accept="image/*" class="border p-2 rounded w-full" />

    <button @click="processImage" :disabled="!selectedFile"
      class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400">
      Upload & Process
    </button>

    <div v-if="loading" class="text-blue-500">
      Processing<span class="dots"></span>
    </div>

    <div v-if="result" class="mt-4 p-3 bg-gray-100 rounded">
      <h3 class="font-semibold">Response:</h3>
      <p class="text-sm">{{ result }}</p>
      <hr>
      <hr>
      <h3 class="font-semibold">Generated Image:</h3>
      <img v-if="outputImage" :src="outputImage" alt="Generated Layout" class="max-w-full h-auto my-2" />
      <hr>
      <h3 class="font-semibold">Extracted Text:</h3>
      <p v-if="extractedText">{{ extractedText }}</p>
      <hr>
      <h3 class="font-semibold">Generated Output:</h3>
      <p v-if="result.generated_text">{{ result.generated_text }}</p>
      <hr>
      <h3 class="font-semibold">Segmentation Mask:</h3>
      <img v-if="segmentationImage" :src="segmentationImage" alt="Segmentation Mask" />
      <hr>
      <h3 class="font-semibold">HTML Layout Generated from Image:</h3>
      <img v-if="outputImage" :src="outputImage" alt="HTML Layout" class="max-w-full h-auto my-2" />
      <hr>
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
      result: "",
      segmentationImage: null,
      outputImage: null,
      extractedText: null,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      console.log("Selected File:", this.selectedFile);
      // Removed redundant call that used response.data outside the promise.
      // The image processing will occur in processImage() when the user clicks the button.
    },
    async processImage() {
      if (!this.selectedFile) {
        alert("Please first choose an image file!");
        return;
      }
      this.loading = true;

      let formData = new FormData();
      formData.append("file", this.selectedFile); // Changed from "image" to "file" to match FastAPI parameter

      try {
        const response = await axios.post("http://127.0.0.1:8001/process_image/", formData, { // Updated URL to match FastAPI endpoint
          headers: { "Content-Type": "multipart/form-data" },
          //  timeout: 120000 // Increase timeout to 2 minutes
        });

        const data = response.data;
        console.log("Server Response:", data); // Debugging Log

        if (data.output_image) {
          // Use the absolute path if available, otherwise fallback to relative path
          this.outputImage = data.absolute_output_path || data.output_image;
        }

        if (data.extracted_text) {
          this.extractedText = Array.isArray(data.extracted_text) ? data.extracted_text.join(" ") : data.extracted_text;
        }

        this.result = data;
      } catch (error) {
        console.error("Error:", error.response?.data || error.message);
        this.result = "Server error. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    // Remove the duplicate uploadImage method
  }
};
</script>

<style scoped>
@keyframes dots {
  0% {
    content: ".";
  }

  33% {
    content: "..";
  }

  66% {
    content: "...";
  }

  100% {
    content: "";
  }
}

.dots::after {
  content: " .";
  animation: dots 1.5s steps(3, end) infinite;
}

button:disabled {
  cursor: not-allowed;
}
</style>