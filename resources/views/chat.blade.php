@extends('layouts.app')

@section('content')
<div id="app">
    <chat-component></chat-component>
    <image-processor></image-processor>
</div>
@endsection

@push('scripts')
<script src="{{ mix('js/app.js') }}"></script>
@endpush