import _ from "lodash";

export function paginate(items, pageNubmer, pageSize) {
  const startIndex = (pageNubmer - 1) * pageSize;
  return _(items).slice(startIndex).take(pageSize).value();
}
