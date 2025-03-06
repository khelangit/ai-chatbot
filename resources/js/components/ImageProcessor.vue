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
      <img v-if="outputImage" :src="outputImage" alt="Generated Layout" />
       <hr>
      <h3>Extracted Text:</h3>
      <p v-if="extractedText">{{ extractedText }}</p>
       <hr>
      <h3>Generated Output:</h3>
      <p v-if="result.generated_text">{{ result.generated_text }}</p>
       <hr>
      <h3>Segmentation Mask:</h3>
      <img v-if="segmentationImage" :src="segmentationImage" alt="Segmentation Mask" />
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
      formData.append("image", this.selectedFile);

      try {
        const response = await fetch("http://127.0.0.1:8001/process-image/", {
          method: "POST",
          body: formData
        });
        const data = await response.json();
        this.result = data;
        console.log('result', data); // Debugging Log

        // Assume the API returns an output_image field and extracted_text as an array.
        this.outputImage = "/storage/" + data.output_image;
        this.extractedText = data.extracted_text.join(" ");
      } catch (error) {
        console.error("Error:", error.response?.data || error.message);
        this.result = "Server error. Please try again.";
      } finally {
        this.loading = false;
      }
    }
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