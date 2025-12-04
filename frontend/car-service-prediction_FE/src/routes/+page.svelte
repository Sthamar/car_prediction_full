<script>
  import { onMount } from 'svelte';
  
  let formData = {
    make: '',
    model: '',
    year: new Date().getFullYear(),
    mileage: 0,
    last_service_date: new Date().toISOString().split('T')[0],
    engine_size: 2.0,
    transmission: 'automatic',
    fuel_type: 'gasoline'
  };
  
  let prediction = null;
  let loading = false;
  let error = null;
  
  const carMakes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes-Benz', 'Audi', 'Nissan', 'Hyundai', 'Volkswagen'];
  
  async function handleSubmit() {
    loading = true;
    error = null;
    prediction = null;
    
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        throw new Error('Prediction failed');
      }
      
      prediction = await response.json();
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }
  
  function getRiskColor(risk) {
    switch(risk) {
      case 'High': return 'bg-red-100 border-red-500 text-red-800';
      case 'Medium': return 'bg-yellow-100 border-yellow-500 text-yellow-800';
      case 'Low': return 'bg-green-100 border-green-500 text-green-800';
      default: return 'bg-gray-100 border-gray-500 text-gray-800';
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
  <div class="max-w-4xl mx-auto">
    <div class="text-center mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">🚗 Car Service Predictor</h1>
      <p class="text-gray-600">AI-powered maintenance predictions for your vehicle</p>
    </div>
    
    <div class="bg-white rounded-lg shadow-xl p-8 mb-6">
      <h2 class="text-2xl font-semibold mb-6 text-gray-800">Vehicle Information</h2>
      
      <form on:submit|preventDefault={handleSubmit} class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Make</label>
            <select bind:value={formData.make} required class="w-full px-4 py-2 border text-primary border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="">Select make...</option>
              {#each carMakes as make}
                <option value={make}>{make}</option>
              {/each}
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Model</label>
            <input type="text" bind:value={formData.model} required class="w-full px-4 py-2 border text-primary border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="e.g., Camry" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Year</label>
            <input type="number" bind:value={formData.year} min="1990" max={new Date().getFullYear() + 1} required class="w-full px-4 py-2 border text-primary border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Mileage</label>
            <input type="number" bind:value={formData.mileage} min="0" step="100" required class="w-full px-4 text-primary py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="e.g., 45000" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Last Service Date</label>
            <input type="date" bind:value={formData.last_service_date} required class="w-full px-4 py-2 border text-primary border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Engine Size (L)</label>
            <input type="number" bind:value={formData.engine_size} min="0.5" max="8" step="0.1" required class="w-full text-primary px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Transmission</label>
            <select bind:value={formData.transmission} required class="w-full px-4 py-2 border border-gray-300 text-primary rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="automatic">Automatic</option>
              <option value="manual">Manual</option>
              <option value="cvt">CVT</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Fuel Type</label>
            <select bind:value={formData.fuel_type} required class="w-full px-4 py-2 border text-primary border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="gasoline">Gasoline</option>
              <option value="diesel">Diesel</option>
              <option value="electric">Electric</option>
              <option value="hybrid">Hybrid</option>
            </select>
          </div>
        </div>
        
        <button type="submit" disabled={loading} class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed mt-6">
          {loading ? 'Analyzing...' : 'Predict Service Needs'}
        </button>
      </form>
    </div>
    
    {#if error}
      <div class="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded">
        <p class="text-red-800">⚠️ Error: {error}</p>
      </div>
    {/if}
    
    {#if prediction}
      <div class="bg-white rounded-lg shadow-xl p-8">
        <h2 class="text-2xl font-semibold mb-6 text-gray-800">Prediction Results</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div class={`p-6 rounded-lg border-l-4 ${getRiskColor(prediction.risk_level)}`}>
            <h3 class="font-semibold text-lg mb-2">Risk Level</h3>
            <p class="text-3xl font-bold">{prediction.risk_level}</p>
          </div>
          
          <div class="p-6 rounded-lg border-l-4 bg-blue-50 border-blue-500">
            <h3 class="font-semibold text-lg mb-2 text-blue-800">Confidence Score</h3>
            <p class="text-3xl font-bold text-blue-800">{(prediction.confidence * 100).toFixed(0)}%</p>
          </div>
          
          <div class="p-6 rounded-lg border-l-4 bg-purple-50 border-purple-500">
            <h3 class="font-semibold text-lg mb-2 text-purple-800">Service Status</h3>
            <p class="text-2xl font-bold text-purple-800">{prediction.service_needed ? '⚠️ Required' : '✅ Not Required'}</p>
          </div>
          
          <div class="p-6 rounded-lg border-l-4 bg-indigo-50 border-indigo-500">
            <h3 class="font-semibold text-lg mb-2 text-indigo-800">Estimated Days</h3>
            <p class="text-3xl font-bold text-indigo-800">{prediction.estimated_days_until_service}</p>
            <p class="text-sm text-indigo-600">days until service</p>
          </div>
        </div>
        
        <div class="bg-gray-50 rounded-lg p-6">
          <h3 class="font-semibold text-lg mb-4 text-gray-800">Recommended Services</h3>
          <ul class="space-y-2">
            {#each prediction.recommended_services as service}
              <li class="flex items-center text-gray-700">
                <span class="text-green-500 mr-2">✓</span>
                {service}
              </li>
            {/each}
          </ul>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  }
</style>