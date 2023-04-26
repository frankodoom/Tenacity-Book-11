import {
  AfterViewInit,
  Component,
  ElementRef,
  HostListener,
  Input,
  NgZone,
  ViewChild,
  ViewEncapsulation,
} from '@angular/core';
import { environment } from 'src/environments/environment';
import * as $ from 'jquery';

@Component({
  selector: 'app-page',
  templateUrl: './page.component.html',
  styleUrls: ['./page.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class PageComponent implements AfterViewInit {
  loadState: 'loading' | 'success' | 'error' = 'loading';
  zoom = 1;
  @ViewChild('container') container!: ElementRef;

  private _pageId: number = 1;
  private resizeDebounceTimeout: any;

  get pageId(): number {
    return this._pageId;
  }
  @Input() set pageId(value: number) {
    this._pageId = value;
    this.loadContent();
  }

  constructor() {}

  ngAfterViewInit() {
    setTimeout(() => {
      this.updateZoom();
    });

    setTimeout(()=>{
      //let output:any = document.getElementsByTagName("iframe");
      //console.log("iframe Html 5")
      // This removes scroll from iframes
      let output:any = $("iframe").contents().find('html.h5p-iframe').each(function(){
        this.scrollTo( 0, this.scrollHeight);
      }).css("overflow","hidden");

    } , 3000)
  }

  loadContent() {
    this.loadState = 'loading';
    fetch(`/assets/pages/${this.pageId}.html`)
      .then((response) => response.text())
      .then((html) => {
        this.container.nativeElement.firstChild.innerHTML = html;
        this.loadState = 'success';

        const mediaElements = $(this.container.nativeElement).find(
          'audio, video'
        );
        mediaElements.on({
          play: function (e: Event) {
            mediaElements.each(function (_index, element: any) {
              if (element != e.target) element.pause();
            });
          },
        });
      })
      .catch((err) => {
        this.loadState = 'error';
        console.error(err);
      });
  }

  handleDoubleClick() {
    if (!environment.production && this.loadState == 'success')
      this.loadContent();
  }

  @HostListener('window:resize')
  onResize() {
    clearTimeout(this.resizeDebounceTimeout);
    this.resizeDebounceTimeout = setTimeout(() => {
      this.updateZoom();
    }, 1000);
  }

  updateZoom() {
    if (this.container) {
      const page: HTMLDivElement = this.container.nativeElement;
      const pageWidth = 955.91;
      this.zoom = Math.min(1, page.parentElement!.clientWidth / pageWidth);
    }
  }
}
