import {
  AfterViewInit,
  Component,
  HostListener,
  Input,
  ViewChild,
  ViewEncapsulation,
} from '@angular/core';
import { CdkVirtualScrollViewport } from '@angular/cdk/scrolling';
import { Page } from '../types';
import * as $ from 'jquery';

@Component({
  selector: 'app-content-viewport',
  templateUrl: './content-viewport.component.html',
  styleUrls: ['./content-viewport.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class ContentViewportComponent implements AfterViewInit {
  pageWidth = 1000;
  @ViewChild('viewport') viewport!: CdkVirtualScrollViewport;
  @Input() pages!: Page[];
  private _page: number = 1;
  private resizeDebounceTimeout: any;

  get page(): number {
    return this._page;
  }

  @Input() set page(value: number) {
    const delta = Math.abs(value - this._page);
    this._page = value;
    if (this.viewport) {
      this.viewport.scrollToIndex(value - 1, delta == 1 ? 'smooth' : undefined);

      // Pause all videos & audio clips
      $(this.viewport.getElementRef().nativeElement)
        .find('audio, video')
        .each(function (_index, element: any) {
          element.pause();
        });
    }
  }

  ngAfterViewInit() {
    window.setTimeout(() => {
      this.updatePageWidth();
    });
  }

  @HostListener('window:resize')
  onResize() {
    clearTimeout(this.resizeDebounceTimeout);
    this.resizeDebounceTimeout = setTimeout(() => {
      this.updatePageWidth();
    }, 1000);
  }

  private updatePageWidth() {
    this.pageWidth = this.viewport.elementRef.nativeElement.clientWidth;
    window.setTimeout(() => {
      this.viewport.scrollToIndex(this._page - 1);
    }, 100);
  }
}
