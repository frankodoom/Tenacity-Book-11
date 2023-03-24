import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import * as dictionary from "./dictionary.json";

@Component({
  templateUrl: './dictionary-popup.component.html',
  styleUrls: ['./dictionary-popup.component.css'],
})
export class DictionaryPopupComponent {
  readonly phonetics?: string;
  readonly lexemes?: any[];
  readonly audioUrl?: string;
  readonly webLink?: string;

  constructor(@Inject(MAT_DIALOG_DATA) public word: string) {
    try {
      const data = (dictionary as any)[word];
      const entry = data.entries[0];
      if (!entry) return;

      this.word = entry.interpretations[0].lemma;
      this.lexemes = entry.lexemes;
      this.webLink = entry.sourceUrls[0];

      if (entry.pronunciations) {
        let index = entry.pronunciations.findIndex((p: any) => p.audio);
        if (index == -1) index = 0;

        const pronunciation = entry.pronunciations[index];
        this.audioUrl = pronunciation.audio?.url;
        if (pronunciation.transcriptions)
          this.phonetics = pronunciation.transcriptions[0].transcription;
      }
    } catch (err) {
      console.error(err);
    }
  }
}
