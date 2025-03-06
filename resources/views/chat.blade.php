@extends('layouts.app')

@section('content')
<div id="app">
    <chat-component></chat-component>
    <image-processor></image-processor>
</div>
@endsection

@push('scripts')
<script src="{{ mix('js/app.js') }}">
    export default {
  data() {
    return {
      showImageProcessor: false
    };
  },
  methods: {
    toggleImageProcessor() {
      this.showImageProcessor = !this.showImageProcessor;
    }
  }
};
</script>
@endpush