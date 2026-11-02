export class AudioManager {
  constructor() {
    this.ctx = null;
    this.buffers = {};
    this.volumes = {};
    this.sourceNodes = [];
    this._initialized = false;
    this._musicSource = null;
    this._musicGain = null;
    this._musicGen = 0;
  }

  init() {
    if (this._initialized) return;
    this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    this._initialized = true;
    this._musicGain = this.ctx.createGain();
    this._musicGain.gain.value = 0.4;
    this._musicGain.connect(this.ctx.destination);
  }

  async loadBuffer(key, url, volume = 0.6) {
    if (!this.ctx) return;
    try {
      const resp = await fetch(url);
      const arrayBuffer = await resp.arrayBuffer();
      const audioBuffer = await this.ctx.decodeAudioData(arrayBuffer);
      this.buffers[key] = audioBuffer;
      this.volumes[key] = volume;
    } catch (e) {
      console.warn(`No se pudo cargar sonido: ${url}`, e);
    }
  }

  async play(key) {
    if (!this.ctx || !this.buffers[key]) return null;
    if (this.ctx.state === 'suspended') {
      try { await this.ctx.resume(); } catch (e) {}
    }
    const source = this.ctx.createBufferSource();
    source.buffer = this.buffers[key];
    const gain = this.ctx.createGain();
    gain.gain.value = this.volumes[key] || 0.6;
    source.connect(gain);
    gain.connect(this.ctx.destination);
    source.start(0);
    this.sourceNodes.push(source);
    source.onended = () => {
      const idx = this.sourceNodes.indexOf(source);
      if (idx >= 0) this.sourceNodes.splice(idx, 1);
    };
    return source;
  }

  stop(key) {
    for (const src of this.sourceNodes) {
      try { src.stop(); } catch(e) {}
    }
    this.sourceNodes = [];
  }

  async playMusic(url, volume = 0.4) {
    if (!this.ctx) return;
    if (this.ctx.state === 'suspended') {
      try { await this.ctx.resume(); } catch (e) {}
    }
    const myGen = ++this._musicGen;
    this.stopMusic();
    try {
      const resp = await fetch(url);
      if (myGen !== this._musicGen) return;
      const arrayBuffer = await resp.arrayBuffer();
      if (myGen !== this._musicGen) return;
      const audioBuffer = await this.ctx.decodeAudioData(arrayBuffer);
      if (myGen !== this._musicGen) return;
      const source = this.ctx.createBufferSource();
      source.buffer = audioBuffer;
      source.loop = true;
      source.connect(this._musicGain);
      this._musicGain.gain.value = volume;
      source.start(0);
      this._musicSource = source;
    } catch (e) {
      console.warn('playMusic failed:', e);
    }
  }

  stopMusic() {
    if (this._musicSource) {
      try { this._musicSource.stop(); } catch(e) {}
      this._musicSource = null;
    }
  }
}
