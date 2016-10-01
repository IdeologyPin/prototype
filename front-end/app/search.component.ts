/**
 * Created by sasinda on 9/10/16.
 */
import {Component} from '@angular/core';

@Component({
    selector: 'search-box',
    template: ` <li>
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                        <input type="text" > <i class="fa fa-search"></i>
                     </a>
                </li>
               `
})
export class SearchComponent {
}