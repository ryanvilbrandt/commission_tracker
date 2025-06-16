/**
 * @jest-environment jsdom
 */

import { renderData } from '../../static/js/commissions';
import { prettyDOM } from '@testing-library/dom';

describe('renderData', () => {
  it('renders expected DOM structure', () => {
    const data = {
      items: [
        { name: 'Item 1' },
        { name: 'Item 2' },
      ]
    };

    const container = renderData(data);

    expect(prettyDOM(container, null, { highlight: false })).toMatchSnapshot();
  });
});