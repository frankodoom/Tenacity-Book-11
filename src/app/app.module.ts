import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material.module';
import { ContentViewportComponent } from './content-viewport/content-viewport.component';
import { PageComponent } from './page/page.component';
import { DictionaryPopupComponent } from './dictionary-popup/dictionary-popup.component';
import { DictationComponent } from './dictation/dictation.component';

@NgModule({
  declarations: [AppComponent, ContentViewportComponent, PageComponent, DictionaryPopupComponent, DictationComponent],
  imports: [BrowserModule, BrowserAnimationsModule, MaterialModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
