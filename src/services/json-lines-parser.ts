import { Transform, TransformCallback } from 'stream';

/**
 * Parses newline-delimited JSON (JSONL) stream
 */
export class JsonLinesParser extends Transform {
  private buffer: string = '';

  constructor() {
    super({ objectMode: true });
  }

  _transform(chunk: Buffer | string, encoding: string, callback: TransformCallback): void {
    // Append new data to buffer
    this.buffer += chunk.toString();
    
    // Split by newlines but keep last incomplete line in buffer
    const lines = this.buffer.split('\n');
    this.buffer = lines.pop() || '';
    
    // Parse each complete line
    for (const line of lines) {
      if (line.trim()) {
        try {
          const parsed = JSON.parse(line);
          this.push(parsed);
        } catch (_error) {
          this.emit('error', new Error(`Invalid JSON: ${line}`));
        }
      }
    }
    
    callback();
  }

  _flush(callback: TransformCallback): void {
    // Process any remaining data when stream ends
    if (this.buffer.trim()) {
      try {
        const parsed = JSON.parse(this.buffer);
        this.push(parsed);
      } catch (_error) {
        this.emit('error', new Error(`Invalid JSON: ${this.buffer}`));
      }
    }
    callback();
  }

  /**
   * Reset the parser state
   */
  reset(): void {
    this.buffer = '';
  }

  /**
   * Get current buffer content (for debugging)
   */
  getBuffer(): string {
    return this.buffer;
  }
}