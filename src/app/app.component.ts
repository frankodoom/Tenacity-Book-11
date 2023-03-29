import {
  Component,
  HostListener,
  Injector,
  NgZone,
  OnInit,
  ViewChild,
} from '@angular/core';
import { CdkVirtualScrollViewport } from '@angular/cdk/scrolling';
import { Page, Section } from './types';
import pageData from './pages';
import * as $ from 'jquery';
import { MatDialog } from '@angular/material/dialog';
import { DictionaryPopupComponent } from './dictionary-popup/dictionary-popup.component';
import { createCustomElement } from '@angular/elements';
import { DictationComponent } from './dictation/dictation.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  title = 'etlearns-book';
  isFullscreen = false;
  isSideNavOpen = false;
  readonly pages: Page[];
  readonly sections: Section[];
  @ViewChild('sidenavScrollViewport')
  sidenavScrollViewport!: CdkVirtualScrollViewport;
  private _currentPage = 1;
  private readonly pagesToSkip : Array<Number>= [];//[121, 178, 234];

  public get currentPage() {
    return this._currentPage;
  }
  public set currentPage(value) {
    if (value > 0 && value <= this.pages.length) {
      if (this.pagesToSkip.includes(value))
        value = this._currentPage > value ? value - 1 : value + 1;

      window.history.pushState(null, '', `/?page=${value}`);
      this._currentPage = value;
      this.isSideNavOpen = false;
    }
  }

  constructor(ngZone: NgZone, injector: Injector, dialog: MatDialog) {
    this.sections = pageData.sections;
    this.pages = pageData.pages;
    this.onUrlChanged();

    (window as any).$ = $;

    // For page links
    (window as any).goToPage = (page: number) => {
      ngZone.run(() => (this.currentPage = page));
    };

    // For dictionary popup
    (window as any).showDictionary = (word: string) => {
      ngZone.run(() =>
        dialog.open(DictionaryPopupComponent, {
          data: word,
          autoFocus: false,
        })
      );
    };

    // Dictation element
    const dictationElementName = 'app-dictation';
    if (!customElements.get(dictationElementName)) {
      const DictationElement = createCustomElement(DictationComponent, {
        injector,
      });
      customElements.define(dictationElementName, DictationElement);
    }
  }

  ngOnInit() {
    this.isFullscreen = !!document.fullscreenElement;
    window.addEventListener('popstate', () => this.onUrlChanged());
  }

  isInSection(section: Section) {
    return section.end
      ? this.currentPage >= section.start && this.currentPage <= section.end
      : this.currentPage == section.start;
  }

  toggleFullscreen() {
    if (this.isFullscreen) document.exitFullscreen();
    else document.documentElement.requestFullscreen();
  }

  toggleSideNav() {
    this.isSideNavOpen = !this.isSideNavOpen;
    if (this.isSideNavOpen) {
      setTimeout(() => {
        this.sidenavScrollViewport.checkViewportSize();
        this.sidenavScrollViewport.scrollToIndex(
          Math.max(0, this.currentPage - 5)
        );
      }, 1);
    }
  }

  @HostListener('window:fullscreenchange')
  onFullscreenStatusChanged() {
    this.isFullscreen = !!document.fullscreenElement;
  }

  onKeyDown(event: KeyboardEvent) {
    if (event.code == 'ArrowLeft') this.currentPage--;
    else if (event.code == 'ArrowRight') this.currentPage++;
  }

  private onUrlChanged() {
    const urlParams = new URLSearchParams(window.location.search);
    const page = urlParams.get('page');
    if (page && !Number.isNaN(page)) this._currentPage = Number.parseInt(page);
  }
}
